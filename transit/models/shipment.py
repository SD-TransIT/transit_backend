from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from transit.models.base import BaseModel
from transit.models.delivery_status import DeliveryStatus
from transit.models.driver import Driver
from transit.models.order_details import OrderDetails
from transit.models.supplier import Supplier
from transit.models.transporter import TransporterDetails


class ShipmentDetailsManager(models.Manager):
    # Simplifies M:N with ShipmentOrderMapping
    @transaction.atomic
    def create(self, *args, **kwargs):
        orders = kwargs.get('orders')
        shipment_orders = self._orders_to_order_objects(orders) if orders else []
        shipment = super(ShipmentDetailsManager, self).create(*args, **kwargs)
        for order in shipment_orders:
            # TODO: M:N relation should be created automatically through django, this should be obsolete
            ShipmentOrderMapping.objects.create(shipment_details=shipment, order_details=order)
        return shipment

    def _orders_to_order_objects(self, orders):
        order_details = []
        for order in orders:
            if isinstance(order, OrderDetails):
                order_details.append(order)
            elif OrderDetails.objects.filter(pk=order).exists():
                order_details.append(OrderDetails.objects.get(order))
            else:
                raise ValueError(
                    _("Cannot bind order detail with code %s to OrderDetail object."
                      "Passed orders should be either OrderDetail object or OrderDetails pk.") % repr(order)
                )
        return order_details


class ShipmentDetails(BaseModel):
    transporter_details = models.ForeignKey(
        TransporterDetails, models.DO_NOTHING, db_column='TransporterDetailsID'
    )
    driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='DriverID')
    supplier = models.ForeignKey(Supplier, models.DO_NOTHING, db_column='SupplierID')

    ship_date = models.DateTimeField(db_column='ShipDate', null=True)
    expected_delivery_date = models.DateTimeField(db_column='ExpectedDeliveryDate', null=True)
    delivery_date = models.DateTimeField(db_column='DeliveryDate', null=True)
    timestamp = models.DateTimeField(db_column='Timestamp', null=True)

    pod = models.BooleanField(db_column="POD", null=True)
    delay_justified = models.BooleanField(db_column="DelayJustified", blank=True, null=True)

    transporter_base_cost = models.DecimalField(
        db_column='TransporterBaseCost', null=True, max_digits=18, decimal_places=2
    )
    number_of_kilometers = models.DecimalField(
        db_column='NumberOfKilometers', null=True, max_digits=18, decimal_places=2
    )
    transporter_per_diem = models.DecimalField(
        db_column='TransporterPerDiem', null=True, max_digits=18, decimal_places=2
    )

    transporter_additional_cost = models.DecimalField(
        db_column='TransporterAdditionalCost', null=True, max_digits=18, decimal_places=2
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


# Impossible to put this function inside of class due to lambda serialization exception
def content_file_name(instance, filename):
    return '/'.join(['shipment', str(instance.shipment.id), filename])


class ShipmentDetailFiles(models.Model):
    shipment = models.ForeignKey(ShipmentDetails, models.CASCADE, db_column='ShipmentDetailsID')
    file = models.FileField(upload_to=content_file_name)

    class Meta:
        managed = True
        db_table = 'ShipmentDetailFiles'
