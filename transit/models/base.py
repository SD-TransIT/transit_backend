from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    last_modified_date = models.DateTimeField(
        db_column='LastModifiedDate', default=datetime.now
    )
    last_modified_by = models.CharField(
        db_column='LastModifiedBy', max_length=255
    )

    class Meta:
        abstract = True


class GeographicalModel(models.Model):
    address_1 = models.CharField(db_column='Address', max_length=255, blank=True, null=True)
    address_2 = models.CharField(db_column='Address2', max_length=255, blank=True, null=True)
    address_3 = models.CharField(db_column='Address3', max_length=255, blank=True, null=True)

    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)
    latitude_longitude = models.CharField(
        db_column='LatitudeLongitude', max_length=255, blank=True, null=True
    )

    class Meta:
        abstract = True
