from django.db import models

from transit.models.base import BaseModel


class PortalAccess(BaseModel):
    username = models.CharField(db_column="UserName", max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PortalAccess'
