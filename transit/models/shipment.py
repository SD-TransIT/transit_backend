from typing import Collection

from django.db import models

from transit.models.base import BaseModel
from transit.models.delivery_status import DeliveryStatus
from transit.models.driver import Driver
from transit.models.order_details import OrderDetails
from transit.models.supplier import Supplier
from transit.models.transporter import TransporterDetails, Transporter


class ShipmentDetailsQueryset(models.QuerySet):

    def transporter_shipments(self, transporter: Transporter):
        return self.filter(transporter_details__transporter=transporter).distinct()

    def vehicle_shipments(self, vehicle: TransporterDetails = None, vehicles: Collection[TransporterDetails] = None):
        """
        Filter ShipmentDetails for shipments relevant for given vehicle or vehicles list.
        Only on of `vehicle` and `vehicles` arguments can be provided. If both are provided ValueError is raised.
        :param vehicle: Object of TransporterDetails type
        :param vehicles: Collection of TransporterDetails instances.
        :return: filtered QuerySet
        """
        if vehicle and vehicles:
            raise ValueError(
                "`vehicles` and `vehicle` arguments cannot be used in the same time in vehicle_shipments"
            )
        vehicles = vehicles if vehicles else [vehicle]

        return self.filter(transporter_details__in=vehicles).distinct()

    def shipments_with_cost(self):
        """
        Filter for shipments that have base_cost different from null.
        :return: filtered QuerySet
        """
        return self.filter(transporter_base_cost__isnull=False)

    def shipments_without_cost(self):
        """
        Filter for shipments that where base_cost is null.
        :return: filtered QuerySet
        """
        return self.filter(transporter_base_cost__isnull=True)


class ShipmentDetailsManager(models.Manager):

    def get_queryset(self):
        return ShipmentDetailsQueryset(self.model, using=self._db)

    def transporter_shipments(self, transporter: Transporter):
        return self.get_queryset().transporter_shipments(transporter)

    def vehicle_shipments(self, vehicle: TransporterDetails = None, vehicles: Collection[TransporterDetails] = None):
        return self.get_queryset().vehicles_shipments(vehicle=vehicle, vehicles=vehicles)

    def shipments_with_cost(self):
        return self.get_queryset().shipments_with_cost()

    def shipments_without_cost(self):
        return self.get_queryset().shipments_without_cost()


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

    objects = ShipmentDetailsManager()

    class Meta:
        managed = True
        db_table = 'ShipmentDetails'


class ShipmentOrderMapping(BaseModel):
    shipment_details = models.ForeignKey(ShipmentDetails, models.CASCADE, db_column='ShipmentDetailsID',
                                         related_name='order_mapping')
    order_details = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column='OrderDetailsID',
                                      related_name='shipment_mapping')

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
