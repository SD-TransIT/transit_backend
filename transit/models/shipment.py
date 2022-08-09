from django.db import models

from transit.models.base import BaseModel
from transit.models.delivery_status import DeliveryStatus
from transit.models.driver import Driver
from transit.models.order_details import OrderDetails
from transit.models.supplier import Supplier
from transit.models.transporter import TransporterDetails


class ShipmentDetails(BaseModel):
    transporter_details = models.ForeignKey(
        TransporterDetails, models.DO_NOTHING, db_column='TransporterDetailsID'
    )
    driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='DriverID')
    supplier = models.ForeignKey(Supplier, models.DO_NOTHING, db_column='SupplierID')

    ship_date = models.DateTimeField(db_column='ShipDate', blank=True, null=True)
    expected_delivery_date = models.DateTimeField(db_column='ExpectedDeliveryDate', blank=True, null=True)
    delivery_date = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)

    pod = models.BooleanField(db_column="POD", blank=True, null=True)
    delay_justified = models.BooleanField(db_column="DelayJustified", blank=True, null=True)

    transporter_base_cost = models.DecimalField(
        db_column='TransporterBaseCost', blank=True, null=True, max_digits=18, decimal_places=2
    )
    number_of_kilometers = models.DecimalField(
        db_column='NumberOfKilometers', blank=True, null=True, max_digits=18, decimal_places=2
    )
    transporter_per_diem = models.DecimalField(
        db_column='TransporterPerDiem', blank=True, null=True, max_digits=18, decimal_places=2
    )

    transporter_additional_cost = models.DecimalField(
        db_column='TransporterAdditionalCost', blank=True, null=True, max_digits=18, decimal_places=2
    )

    shipment_status = models.IntegerField(db_column='ShipmentStatus', blank=True, null=True)
    delivery_status = models.ForeignKey(
        DeliveryStatus, models.DO_NOTHING, db_column='DeliveryStatus', related_name='delivery_status_master'
    )
    pod_status = models.ForeignKey(
        DeliveryStatus, models.DO_NOTHING, db_column='PODStatus', related_name='delivery_status_master1'
    )

    custom_route_number = models.CharField(db_column='CustomRouteNumber', max_length=50, blank=True, null=True)
    gps_coordinates = models.CharField(db_column='GPSCoordinates', max_length=50, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)
    ropo_number = models.CharField(db_column='ROPONumber', max_length=255, blank=True, null=True)
    signed_by = models.CharField(db_column='SignedBy', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ShipmentDetails'


class ShipmentOrderMapping(BaseModel):
    shipment_details = models.ForeignKey(ShipmentDetails, models.DO_NOTHING, db_column='ShipmentDetailsID')
    order_details = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column='OrderDetailsID')

    class Meta:
        managed = True
        db_table = 'ShipmentOrderMapping'
