from django.db import models

from transit.models.base import (
    BaseModel,
    GeographicalModel
)


class CustomerType(BaseModel):
    customer_type_name = models.CharField(
        db_column='CustomerTypeName', max_length=255, blank=True, null=True, unique=True
    )

    class Meta:
        managed = True
        db_table = 'CustomerType'


class Customer(BaseModel, GeographicalModel):
    name = models.CharField(db_column='CustomerName', max_length=255)
    first_name = models.CharField(db_column='FirstName', max_length=255, null=True, blank=True)
    last_name = models.CharField(db_column='LastName', max_length=255, null=True, blank=True)
    phone = models.CharField(db_column='Phone', max_length=255, null=True, blank=True)
    email = models.CharField(db_column='Email', max_length=255, null=True, blank=True)

    customer_type = models.ForeignKey(
        CustomerType, models.DO_NOTHING, db_column='CustomerTypeID'
    )

    class Meta:
        managed = True
        db_table = 'Customer'


class CustomerWeekDays(BaseModel):
    customer = models.ForeignKey(
        Customer, models.CASCADE, db_column='CustomerID', related_name='week_days'
    )
    day = models.IntegerField(db_column='Day')
    opening_time = models.CharField(db_column='OpeningTime', max_length=50, default="N/A")
    closing_time = models.CharField(db_column='ClosingTime', max_length=50, default="N/A")
    closed = models.BooleanField(
        db_column='Closed', default=False, null=True
    )

    meridiem_indicator_opening_time = models.CharField(
        db_column='Meridiem_Indicator_OpeningTime', max_length=20, blank=True, null=True
    )
    meridiem_indicator_closing_time = models.CharField(
        db_column='Meridiem_Indicator_ClosingTime', max_length=20, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = 'CustomerWeekDays'
