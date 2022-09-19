
import logging

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.fields import ListField
from rest_framework.response import Response

from transit.models import OrderDetails, ShipmentDetails, ShipmentOrderMapping, OrderLineDetails
from transit.rest_api.abstract import BaseGenericViewSet
from transit.services.shipment_orders_service import ShipmentOrdersService

logger = logging.getLogger(__name__)


class ShipmentOrderDetailsField(ListField):

    def to_internal_value(self, data):  # noqa: WPS122
        return OrderDetails.objects.get(pk=data)

    def to_representation(self, value: ShipmentOrderMapping):  # noqa: WPS122
        order_lines = value.order_details
        relevant_line_items = OrderLineDetails.objects\
            .filter(order_details=order_lines).all()\
            .values("product__name", "pk")
        return {
            'order': order_lines.order_details_id,
            'line_items': list(relevant_line_items)
        }


class ShipmentOrderDetailsSerializer(serializers.Serializer):
    """
    Serializer added only for generating schema definition. Shipment Order Definitions are managed
    through custom actions.
    """
    _shipment_orders_handler = ShipmentOrdersService()

    def update(self, instance, validated_data):
        raise NotImplementedError("Default actions not available in ShipmentOrderDetailsSerializer serializer.")

    def create(self, validated_data):
        raise NotImplementedError("Default actions not available in ShipmentOrderDetailsSerializer serializer.")

    def add_items(self):
        self._shipment_orders_handler\
            .add_orders_to_shipment(shipment=self.instance, orders=self.validated_data['orders'])

    def remove_items(self):
        self._shipment_orders_handler\
            .remove_orders_from_shipment(shipment=self.instance, orders=self.validated_data['orders'])

    def replace_items(self):
        self._shipment_orders_handler\
            .replace_shipment_orders(shipment=self.instance, orders=self.validated_data['orders'])

    def to_representation(self, instance):
        field = self.fields['orders']
        return field.to_representation(instance.order_mapping.all())

    orders = serializers.ListField(
        child=ShipmentOrderDetailsField(), required=True, allow_empty=False
    )  # Ids of orders relevant for given shipment, handled by ShipmentDetails manager.

    class Meta:
        model = ShipmentDetails
        fields = '__all__'
        ordering = ['-id']


class ShipmentOrderDetailsViewSet(BaseGenericViewSet):
    queryset = ShipmentDetails.objects.all().order_by('-id')

    @action(detail=True, methods=['post'])
    def add_orders_to_shipment(self, request, pk=None):
        serializer = self._build_serializer(request)
        serializer.add_items()
        return self._valid_shipment_orders(serializer)

    @action(detail=True, methods=['post'])
    def remove_orders_from_shipment(self, request, pk=None):
        serializer = self._build_serializer(request)
        serializer.remove_items()
        return self._valid_shipment_orders(serializer)

    @action(detail=True, methods=['post'])
    def replace_orders_in_shipment(self, request, pk=None):
        serializer = self._build_serializer(request)
        serializer.replace_items()
        return self._valid_shipment_orders(serializer)

    def _build_serializer(self, request):
        shipment = self.get_object()
        serializer = self.get_serializer_class()(instance=shipment, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return serializer

    def _valid_shipment_orders(self, serializer):
        return Response(serializer.to_representation(self.get_object()), status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return ShipmentOrderDetailsSerializer
