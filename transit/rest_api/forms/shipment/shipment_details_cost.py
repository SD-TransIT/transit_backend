import logging

from rest_framework.decorators import action
from rest_framework.response import Response

from transit.models import ShipmentDetails
from transit.rest_api.abstract import BaseGenericViewSet
from transit.rest_api.forms.shipment.shipment_details import ShipmentDetailsSerializer

logger = logging.getLogger(__name__)


class ShipmentDetailsCostViewSet(BaseGenericViewSet):
    queryset = ShipmentDetails.objects.all().order_by('-id')

    @action(detail=False, methods=['get'])
    def get_shipments_without_cost(self, request, pk=None):
        shipments = self._shipments_without_cost()
        serializer = self.get_serializer_class()(shipments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_shipments_with_cost(self, request, pk=None):
        shipments = self._shipments_with_cost()
        serializer = self.get_serializer_class()(shipments, many=True)
        return Response(serializer.data)

    def _shipments_without_cost(self):
        shipment_qs = self.get_queryset().shipments_without_cost()
        return self._apply_query_filters(shipment_qs)

    def _shipments_with_cost(self):
        shipment_qs = self.get_queryset().shipments_with_cost()
        return self._apply_query_filters(shipment_qs)

    def _apply_query_filters(self, shipment_qs):
        vehicle = self.request.query_params.get('vehicle')
        vehicles = self.request.query_params.get('vehicles')
        transporter = self.request.query_params.get('transporter')
        if vehicle:
            shipment_qs = shipment_qs.vehicle_shipments(vehicle=vehicle)
        if vehicles:
            shipment_qs = shipment_qs.vehicle_shipments(vehicles=vehicles.split(','))
        if transporter:
            shipment_qs = shipment_qs.transporter_shipments(transporter=transporter)
        return shipment_qs  # noqa: R504

    def get_serializer_class(self):
        return ShipmentDetailsSerializer
