from django.db import models

from transit.models.base import BaseModel
from transit.models.customer import Customer
from transit.models.item import (
    Item,
    ItemDetails
)


class OrderDetailsQueryset(models.QuerySet):
    def with_shipment_details(self):
        return self.filter(shipment_mapping__isnull=False)

    def without_shipment_details(self):
        return self.filter(shipment_mapping__isnull=True)


class OrderDetailsManager(models.Manager):
    def get_queryset(self):
        return OrderDetailsQueryset(self.model, using=self._db)

    def with_shipment_details(self):
        return self.get_queryset().with_shipment_details()

    def without_shipment_details(self):
        return self.get_queryset().without_shipment_details()


class OrderDetails(BaseModel):
    order_details_id = models.CharField(
        max_length=64, primary_key=True, unique=True,
        db_column='OrderDetailsID', blank=False, null=False
    )

    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerID')
    order_received_date = models.CharField(
        db_column='OrderReceivedDate', max_length=255, blank=True, null=True
    )

    objects = OrderDetailsManager()

    class Meta:
        managed = True
        db_table = 'OrderDetails'


class OrderLineDetails(BaseModel):
    order_details = models.ForeignKey(
        OrderDetails, on_delete=models.CASCADE, db_column='OrderDetailsID', related_name='line_items')

    # TODO - product (item) and item details could be fixed, we could keep one of them only
    #  Only details should be stored. Product is redundant.
    product = models.ForeignKey(Item, models.DO_NOTHING, db_column='ProductID')
    item_details = models.ForeignKey(ItemDetails, models.DO_NOTHING, db_column='ItemDetailsID')
    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=2)
    old_quantity = models.DecimalField(
        db_column='OldQuantity', max_digits=18, decimal_places=2, null=True
    )

    class Meta:
        managed = True
        db_table = 'OrderLineDetails'


class OrderStatus(BaseModel):
    status = models.CharField(db_column='Status', max_length=255)

    class Meta:
        managed = True
        db_table = 'OrderStatus'
