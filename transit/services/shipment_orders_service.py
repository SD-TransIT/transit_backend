from typing import Collection

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
    def add_orders_to_shipment(self, shipment: ShipmentDetails, orders: Collection[OrderDetails]):
        """
        Create ShipmentOrderMapping objects for shipment and orders. Provided `orders` must not be assigned to
        already created shipment. All orders have to be assigned to single customer.

        :param shipment: ShipmentDetails to which orders will be assigned.
        :param orders: List of OrderDetails elements. Orders have to have same customer assigned to them.
        :return: Collection of ShipmentOrderMapping
        """
        self._create_orders(shipment, orders)
        self._validate_customers(shipment.order_mapping.all())
        return shipment.order_mapping

    @transaction.atomic
    def remove_orders_from_shipment(self, shipment: ShipmentDetails, orders: Collection[OrderDetails]):
        """
        Delete ShipmentOrderMapping related to provided `orders`.

        :param shipment: ShipmentDetails from which orders are removed. .
        :param orders: List of OrderDetails elements.
        :return: Collection of ShipmentOrderMapping of shipments that are still assigned to shipment.
        """
        self._remove_orders_from_shipment(shipment, orders)
        return shipment.order_mapping

    @transaction.atomic
    def replace_shipment_orders(self, shipment: ShipmentDetails, orders: Collection[OrderDetails]):
        """
        Overwrite ShipmentOrderMapping fpr given shipment with orders. If any prior orders were assigned to
        shipment and are not part of orders - they will be removed.

        :param shipment: Shipment to which orders will be assigned.
        :param orders: List of OrderDetails elements. Orders have to have same customer assigned to them.
        :return: Collection of ShipmentOrderMapping
        """
        # Remove orders that are existing for shipment but not part of payload
        self._remove_orders_from_shipment(shipment, orders, inverse=True)
        # Add new shipment orders
        new_orders = self._get_orders_without_shipment(orders)
        self._create_orders(shipment, new_orders)
        self._validate_customers(shipment.order_mapping.all())
        return shipment.order_mapping

    def _remove_orders_from_shipment(self, shipment: ShipmentDetails, orders: Collection[OrderDetails], inverse=False):
        # Remove shipment orders that are in orders list
        # If reverse=True - all shipments that are not in orders list are removed
        existing_orders = self._get_orders_with_shipment(orders)
        filter_query = Q(order_details__pk__in=[order.pk for order in existing_orders])
        orders_to_remove_query = filter_query if not inverse else ~filter_query
        shipment.order_mapping.all().filter(orders_to_remove_query).delete()

    def _create_orders(self, shipment, orders):
        self._validate_new_orders(orders)
        for order in orders:
            # TODO: M:N relation should be created automatically through django, this should be obsolete
            ShipmentOrderMapping.objects.create(shipment_details=shipment, order_details=order)

    def _validate_new_orders(self, orders):
        new_orders = list(self._get_orders_without_shipment(orders))
        if len(new_orders) != len(orders):
            raise serializers.ValidationError(
                _("Part of provided order details already assigned to shipment: %s." %
                  str(list(self._get_orders_with_shipment(orders))))
            )

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
