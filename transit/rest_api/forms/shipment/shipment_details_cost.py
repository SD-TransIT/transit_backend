import logging

import django_filters
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.decorators import action

from rest_framework.fields import CharField
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from transit.models import OrderDetails, OrderLineDetails, ShipmentDetails
from transit.models.shipment import ShipmentDetailsManager
from transit.rest_api.abstract import BaseModelFormViewSet, BaseGenericViewSet, BaseApiSetView
from transit.rest_api.forms.shipment.shipment_details import ShipmentDetailsSerializer
from transit.services.shipment_orders_service import ShipmentOrdersService

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
        shipment_qs = self._apply_query_filters(shipment_qs)
        return shipment_qs

    def _shipments_with_cost(self):
        shipment_qs = self.get_queryset().shipments_with_cost()
        shipment_qs = self._apply_query_filters(shipment_qs)
        return shipment_qs

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
        return shipment_qs

    def get_serializer_class(self):
        return ShipmentDetailsSerializer
