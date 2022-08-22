from django.db import models

from transit.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Item(BaseModel):
    class Condition(models.TextChoices):  # noqa: WPS141
        UNKNOWN = '', ''
        COLD_CHAIN = 'ColdChain', _('Cold Chain')
        AMBIENT = 'Ambient', _('Ambient')

    name = models.CharField(
        db_column='CompositeProductName', max_length=255, blank=True, null=True
    )

    volume = models.DecimalField(
        db_column='volume', blank=True, null=True, max_digits=18, decimal_places=2
    )
    cost = models.DecimalField(
        db_column='Cost', blank=True, null=True, max_digits=18, decimal_places=2
    )
    weight = models.DecimalField(
        db_column='Weight', blank=True, null=True, max_digits=18, decimal_places=2
    )

    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)
    sub_category = models.CharField(db_column='SubCategory', max_length=255, blank=True, null=True)
    conditions = models.CharField(
        db_column='Conditions',
        max_length=255,
        choices=Condition.choices,
        default=Condition.UNKNOWN,
        null=True
    )

    class Meta:
        managed = True
        db_table = 'Item'


class ItemDetails(BaseModel):
    batch_number = models.CharField(db_column='BatchNumber', max_length=255, null=False, blank=False)

    expiry_date = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)
    manufacturing_date = models.DateTimeField(db_column='ManufacturingDate', blank=True, null=True)
    received_date = models.DateTimeField(db_column='ReceivedDate', blank=True, null=True)

    gtin = models.BigIntegerField(db_column="GTIN", blank=True, null=True)
    lot_number = models.CharField(db_column='LotNumber', max_length=255, blank=True, null=True)
    serial_number = models.CharField(db_column='SerialNumber', max_length=255, blank=True, null=True)

    funding_source = models.CharField(db_column='FundingSource', max_length=255, blank=True, null=True)

    item = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemID', related_name='item_details')  # noqa: WPS120

    class Meta:
        managed = True
        db_table = 'ItemDetails'
