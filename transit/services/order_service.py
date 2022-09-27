from typing import Collection

from django.db import transaction

from transit.models import OrderDetails, OrderLineDetails


class OrderLineItemsService:

    @transaction.atomic
    def replace_order_line_items(self, order: OrderDetails, line_items: Collection[OrderLineDetails]):
        """
        Overwrite OrderLine items for given order with `line items`. If any prior `line items` were assigned to
        order and are not part of line items - they will be removed.

        :param order: order to which line items will be assigned.
        :param line_items: List of OrderLine items elements.
        :return: Collection of OrderLine items
        """
        # Remove line items that are existing for order but not part of payload
        self._remove_all_order_items(order)
        # Add new order line items
        self._create_new_line_items(order, line_items)
        return order.line_items

    def _remove_all_order_items(self, order: OrderDetails):
        not_included = OrderLineDetails.objects.filter(order_details=order)
        not_included.all().delete()

    def _create_new_line_items(self, order: OrderDetails, line_items: Collection[OrderLineDetails]):
        for item in line_items:
            item.order_details = order
        OrderLineDetails.objects.bulk_create(line_items)
