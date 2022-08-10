from django.db import models

from transit.models.base import BaseModel
from transit.models.customer import Customer
from transit.models.item import (
    Item,
    ItemDetails
)


class OrderDetails(BaseModel):
    order_details_id = models.CharField(
        max_length=50, primary_key=True, unique=True, db_column='OrderDetailsID'
    )

    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerID')
    order_received_date = models.CharField(
        db_column='OrderReceivedDate', max_length=255, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = 'OrderDetails'


class OrderLineDetails(BaseModel):
    order_details = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column='OrderDetailsID')

    # TODO - product (item) and item details could be fixed, we could keep one of them only
    product = models.ForeignKey(Item, models.DO_NOTHING, db_column='ProductID')
    item_details = models.ForeignKey(ItemDetails, models.DO_NOTHING, db_column='ItemDetailsID')
    quantity = models.DecimalField(
        db_column='Quantity', blank=True, null=True, max_digits=18, decimal_places=2
    )
    old_quantity = models.DecimalField(
        db_column='OldQuantity', blank=True, null=True, max_digits=18, decimal_places=2
    )

    class Meta:
        managed = True
        db_table = 'OrderLineDetails'


class OrderStatus(BaseModel):
    status = models.CharField(db_column='Status', max_length=255)

    class Meta:
        managed = True
        db_table = 'OrderStatus'
