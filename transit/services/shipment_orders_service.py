from collections.abc import Collection

from django.db import transaction
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from transit.models import OrderDetails
from transit.models.shipment import ShipmentOrderMapping, ShipmentDetails


class ShipmentOrdersService:
    """
    Service allowing CRUD operations on ShipmentDetails, it's created due to ShipmentMapping, which
    should be automatic field in django, but it's manually predetermined in legacy structure.
    """

    @transaction.atomic
    def create(self, shipment: ShipmentDetails, orders: Collection[OrderDetails]):
        new_orders = list(self._get_orders_without_shipment(orders))
        if len(new_orders) != len(orders):
            raise serializers.ValidationError(
                _("Some of provided shipment details already assigned to shipment: %s." %
                  str(list(self._get_orders_with_shipment(orders))))
            )
        self._create_orders(shipment, new_orders)
        self._validate_customers(shipment.order_mapping.all())
        return shipment.order_mapping

    @transaction.atomic
    def update(self, shipment: ShipmentDetails, orders: Collection[OrderDetails]):
        # Remove orders that are existing for shipment but not part of payload
        existing_orders = self._get_orders_with_shipment(orders)
        orders_to_remove_query = ~Q(order_details__pk__in=[order.pk for order in existing_orders])
        shipment.order_mapping.all().filter(orders_to_remove_query).delete()
        # Add new shipment orders
        new_orders = self._get_orders_without_shipment(orders)
        self._create_orders(shipment, new_orders)
        self._validate_customers(shipment.order_mapping.all())
        return shipment.order_mapping

    def _create_orders(self, shipment, orders):
        for order in orders:
            # TODO: M:N relation should be created automatically through django, this should be obsolete
            ShipmentOrderMapping.objects.create(shipment_details=shipment, order_details=order)

    def _get_orders_with_shipment(self, orders):
        return OrderDetails.objects.filter(pk__in=[order.pk for order in orders]).with_shipment_details().all()

    def _get_orders_without_shipment(self, orders):
        return OrderDetails.objects.filter(pk__in=[order.pk for order in orders]).without_shipment_details().all()

    def _validate_customers(self, shipment_order_mappings_queryset: QuerySet[ShipmentOrderMapping]):
        if not shipment_order_mappings_queryset.exists():
            return
        customers = list({order.order_details.customer for order in shipment_order_mappings_queryset})
        customers = sorted(customers, key=lambda x: x.pk)
        if len(customers) != 1:
            raise serializers.ValidationError(
                _("All orders assigned to order have to be assigned to same customers. "
                  "Provided orders are assigned to multiple customers: %s" % (str(customers)))
            )
