import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import ShipmentDetails, OrderDetails
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.permissions import IsFormsClerk


class ShipmentDetailsSerializer(serializers.ModelSerializer):
    last_modified_by = serializers.HiddenField(default=None)

    orders = serializers.ListField(
        child=serializers.ModelField(model_field=OrderDetails()._meta.pk),
        required=False, allow_empty=True
    )  # Ids of orders relevant for given shipment, handled by ShipmentDetails manager.

    class Meta:
        model = ShipmentDetails
        fields = "__all__"
        ordering = ['-id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['last_modified_by'] = user
        return super(ShipmentDetailsSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['last_modified_by'] = user.pk
        return super(ShipmentDetailsSerializer, self).update(instance, validated_data)

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

    def get_serializer_class(self):
        return ShipmentDetailsSerializer
