from django.db import models

from transit.models.base import (
    BaseModel,
    GeographicalModel
)


class Supplier(BaseModel, GeographicalModel):
    name = models.CharField(db_column='Name', max_length=255, null=False, blank=False)
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Supplier'
