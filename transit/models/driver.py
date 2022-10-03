from django.db import models

from transit.models.base import BaseModel
from transit.models.transporter import Transporter


class Driver(BaseModel):
    name = models.CharField(db_column='DriverName', max_length=255)
    username = models.CharField(db_column='Username', max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)

    transporter = models.ForeignKey(Transporter, models.DO_NOTHING, db_column='TransporterID', related_name='drivers')

    class Meta:
        managed = True
        db_table = 'Driver'
