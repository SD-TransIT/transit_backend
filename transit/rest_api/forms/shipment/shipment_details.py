import logging

import django_filters
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.fields import CharField
from rest_framework.response import Response

from transit.models import OrderDetails, OrderLineDetails, ShipmentDetails
from transit.rest_api.abstract import BaseModelFormViewSet
from transit.services.shipment_add_costs_service import ShipmentAddCostsService
from transit.services.shipment_orders_service import ShipmentOrdersService

logger = logging.getLogger(__name__)


class ShipmentOrderMappingOrderNamesReadonlyField(CharField):
    def to_representation(self, value):  # noqa: WPS122
        order_lines = OrderDetails.objects.filter(shipment_mapping__in=value.all()).all()
        relevant_line_items = OrderLineDetails.objects\
            .filter(order_details__in=order_lines).all()\
            .values_list("product__name", flat=True)
        return list(relevant_line_items)


class ShipmentOrderMappingOrderNumbersReadonlyField(CharField):
    def to_representation(self, value):  # noqa: WPS122
        order_details_ids = OrderDetails.objects.filter(shipment_mapping__in=value.all()).all()\
            .values_list('order_details_id', flat=True)
        return list(order_details_ids)


class ShipmentOrderMappingCustomerNamesReadonlyField(CharField):
    def to_representation(self, value):  # noqa: WPS122
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
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    transporter_name = serializers.CharField(source='transporter_details.transporter.name', read_only=True)
    transporter_id = serializers.CharField(source='transporter_details.transporter.id', read_only=True)
    vehicle_number = serializers.CharField(source='transporter_details.vehicle_number', read_only=True)
    customer_name = ShipmentOrderMappingCustomerNamesReadonlyField(source='order_mapping', read_only=True)
    order_names = ShipmentOrderMappingOrderNamesReadonlyField(source='order_mapping', read_only=True)
    order_ids = ShipmentOrderMappingOrderNumbersReadonlyField(source='order_mapping', read_only=True)

    orders = serializers.ListField(
        child=serializers.ModelField(model_field=OrderDetails()._meta.pk),
        required=False, allow_empty=True
    )  # Ids of orders relevant for given shipment, handled by ShipmentDetails manager.

    class Meta:
        model = ShipmentDetails
        fields = '__all__'
        ordering = ['-id']

    @transaction.atomic
    def create(self, validated_data):
        orders = self._orders_from_validated_data(validated_data)
        shipment = super(ShipmentDetailsSerializer, self).create(validated_data)
        self._shipment_orders_handler.add_orders_to_shipment(shipment, orders)
        return shipment

    @transaction.atomic
    def update(self, instance, validated_data):
        orders = self._orders_from_validated_data(validated_data)
        shipment = super(ShipmentDetailsSerializer, self).update(instance, validated_data)
        self._shipment_orders_handler.replace_shipment_orders(shipment, orders)
        return shipment

    def _orders_from_validated_data(self, validated_data):
        user = self.context['request'].user
        validated_data['last_modified_by'] = user.pk
        orders_pks = validated_data.pop('orders', [])
        return OrderDetails.objects.filter(pk__in=orders_pks)


class ShipmentDetailsFilter(django_filters.FilterSet):

    class Meta:
        model = ShipmentDetails
        fields = {
            'ship_date': ['exact', 'lte', 'gte'],
            'expected_delivery_date': ['exact', 'lte', 'gte'],
            'delivery_date': ['exact', 'lte', 'gte'],
            'transporter_base_cost': ['exact', 'lte', 'gte', 'isnull'],
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


class ShipmentAddCostsSerializerWrapper(serializers.ModelSerializer):
    """
        Utilizes ShipmentDetailsSerializer for purpose of bulk update of shipments costs.
    """
    _service = ShipmentAddCostsService()

    id = serializers.IntegerField()

    def update(self, instance, validated_data):
        raise NotImplementedError('update() not supported in ShipmentAddCostsSerializer,'
                                  ' data should be alternated using add_cost_to_shipment')

    def create(self, validated_data):
        raise NotImplementedError('create() not supported in ShipmentAddCostsSerializer,'
                                  ' data should be alternated using add_cost_to_shipment')

    def add_cost_to_shipment(self):
        shipment = dict(self.validated_data)
        self._service.add_cost_to_shipment(shipment=shipment)

    class Meta:
        model = ShipmentDetails
        fields = [
            'id', 'transporter_base_cost',
            'transporter_additional_cost', 'number_of_kilometers',
        ]
        ordering = ['-id']


class ShipmentDetailsViewSet(BaseModelFormViewSet):
    filterset_class = ShipmentDetailsFilter
    queryset = ShipmentDetails.objects.all().order_by('-id')
    search_fields = [
        'id', 'transporter_details__transporter__name', 'driver__name', 'transporter_details__vehicle_number',
        'ship_date', 'expected_delivery_date', 'custom_route_number', 'delay_justified', 'delivery_date',
        'delivery_status__delivery_status', 'pod_status__delivery_status', 'pod',
        'order_mapping__order_details__customer__name'
    ]

    _add_cost_shipment_serializer = ShipmentAddCostsSerializerWrapper

    def get_serializer_class(self):
        return ShipmentDetailsSerializer

    @swagger_auto_schema(methods=['put'], request_body=_add_cost_shipment_serializer)
    @action(detail=False, methods=['put'])
    def add_costs_to_shipment(self, request, *args, **kwargs):
        shipment_add_costs_result = self._create_inputs(request.data)
        return Response(shipment_add_costs_result, status=status.HTTP_200_OK)

    @transaction.atomic
    def _create_inputs(self, list_of_shipments):
        outputs = []
        for shipment in list_of_shipments:
            serializer = self._add_cost_shipment_serializer(data=shipment, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.add_cost_to_shipment()
            outputs.append(serializer.data)
        return outputs
