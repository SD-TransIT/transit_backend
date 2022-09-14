import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, filters
from rest_framework.fields import Field, CharField
from rest_framework.parsers import MultiPartParser

from transit.models import ShipmentDetails, OrderDetails, OrderLineDetails
from transit.models.shipment import ShipmentDetailFiles, ShipmentOrderMapping
from transit.rest_api.abstract import BaseFormViewSet
from transit.services.shipment_orders_service import ShipmentOrdersService
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ShipmentOrderMappingOrderNamesReadonlyField(CharField):
    def to_representation(self, value):
        order_lines = OrderDetails.objects.filter(shipment_mapping__in=value.all()).all()
        relevant_line_items = OrderLineDetails.objects\
            .filter(order_details__in=order_lines).all()\
            .values_list("product__name", flat=True)
        return list(relevant_line_items)


class ShipmentOrderMappingCustomerNamesReadonlyField(CharField):
    def to_representation(self, value):
        customer = OrderDetails.objects.filter(shipment_mapping__in=value.all())\
            .values_list('customer__name', flat=True)
        if customer.count() > 1:
            logger.error("ShipmentOrderMapping %s has multiple customer assigned."
                         "All orders in scope of one shipment should be related to single customer."
                         "Please fix this. ", str(value))
        return customer.first()


class ShipmentDetailsSerializer(serializers.ModelSerializer):
    _shipment_orders_handler = ShipmentOrdersService()

    last_modified_by = serializers.HiddenField(default=None)
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    transporter_name = serializers.CharField(source='transporter_details.name', read_only=True)
    vehicle_number = serializers.CharField(source='transporter_details.vehicle_number', read_only=True)
    customer_name = ShipmentOrderMappingCustomerNamesReadonlyField(source='order_mapping', read_only=True)
    order_names = ShipmentOrderMappingOrderNamesReadonlyField(source='order_mapping', read_only=True)

    orders = serializers.ListField(
        child=serializers.ModelField(model_field=OrderDetails()._meta.pk),
        required=False, allow_empty=True
    )  # Ids of orders relevant for given shipment, handled by ShipmentDetails manager.

    class Meta:
        model = ShipmentDetails
        fields = '__all__'
        ordering = ['-id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['last_modified_by'] = user
        orders_pks = validated_data.pop('orders', None)
        orders = OrderDetails.objects.filter(pk__in=orders_pks)
        shipment = super(ShipmentDetailsSerializer, self).create(validated_data)
        self._shipment_orders_handler.create(shipment, orders)
        return shipment

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['last_modified_by'] = user.pk
        orders_pks = validated_data.pop('orders', [])
        orders = OrderDetails.objects.filter(pk__in=orders_pks)
        shipment = super(ShipmentDetailsSerializer, self).update(instance, validated_data)
        self._shipment_orders_handler.update(shipment, orders)
        return shipment

    def validate(self, data): # noqa: WPS-122
        """
        Ensure orders are not updated directly from shipment endpoint.
        """
        self._orders_not_updatable(data)
        return data

    def _orders_not_updatable(self, shipment_data):
        if self.instance and shipment_data.get('orders'):
            raise serializers.ValidationError(
                _("Shipment Orders have to be updated using shipment_order endpoint.")
            )
        return shipment_data


class ShipmentDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = ShipmentDetails
        fields = {
            'ship_date': ['exact', 'lte', 'gte'],
            'expected_delivery_date': ['exact', 'lte', 'gte'],
            'delivery_date': ['exact', 'lte', 'gte'],
            'transporter_base_cost': ['exact', 'lte', 'gte'],
            'number_of_kilometers': ['exact', 'lte', 'gte'],
            'transporter_per_diem': ['exact', 'lte', 'gte'],
            'transporter_additional_cost': ['exact', 'lte', 'gte'],
            'shipment_status': ['exact'],
            'ropo_number': ['exact'],
            'custom_route_number': ['iexact'],
            'signed_by': ['iexact', 'icontains'],
            'pod': ['exact'],
            'delay_justified': ['exact'],
        }


class ShipmentDetailsViewSet(BaseFormViewSet):
    filterset_class = ShipmentDetailsFilter
    queryset = ShipmentDetails.objects.all().order_by('-id')
    search_fields = [
        'id', 'transporter_details__transporter__name', 'driver__name', 'transporter_details__vehicle_number',
        'ship_date', 'expected_delivery_date', 'custom_route_number', 'delay_justified', 'delivery_date',
        'delivery_status__delivery_status', 'pod_status__delivery_status', 'pod',
        'order_mapping__order_details__customer__name'
    ]

    def get_serializer_class(self):
        return ShipmentDetailsSerializer


class ShipmentDetailFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetailFiles
        fields = ('id', 'shipment', 'file')
        read_only_fields = ['id']
        ordering = ['-id']


class ShipmentDetailFilesViewSet(BaseFormViewSet):
    parser_classes = (MultiPartParser,)
    queryset = ShipmentDetailFiles.objects.all()
    serializer_class = ShipmentDetailFilesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['shipment__id']

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')
