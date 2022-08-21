from django.db import models

from transit.models.base import (
    BaseModel,
    GeographicalModel
)


class ModeOfTransport(BaseModel):
    class_mode = models.CharField(db_column="Class", max_length=255, blank=True, null=True)
    vehicle_type = models.CharField(db_column='VehicleType', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ModeOfTransport'


class Transporter(BaseModel, GeographicalModel):
    # ModeOfTransport is no more need here in that part according to the demo (in legacy code there is field)
    name = models.CharField(db_column='TransporterName', max_length=255)
    phone = models.CharField(db_column="Phone", max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Transporter'


class TransporterDetails(BaseModel):
    transporter = models.ForeignKey(
        Transporter, models.DO_NOTHING, db_column='TransporterID'
    )

    vehicle_number = models.CharField(
        db_column='VehicleNumber', max_length=255, blank=True, null=True
    )
    vehicle_capacity_volume = models.CharField(
        db_column="VehicleCapacityVolume", max_length=255, blank=True, null=True
    )
    vehicle_capacity_weight = models.CharField(
        db_column="VehicleCapacityWeight", max_length=255, blank=True, null=True
    )

    mode_of_transport = models.ForeignKey(
        ModeOfTransport, models.DO_NOTHING,
        db_column='ModeOfTransportID'
    )

    class Meta:
        managed = True
        db_table = 'TransporterDetails'
