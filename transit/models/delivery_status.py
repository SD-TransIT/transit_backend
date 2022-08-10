from django.db import models


class DeliveryStatus(models.Model):
    delivery_status_key = models.CharField(
        max_length=50, primary_key=True, unique=True, db_column='DeliveryStatusKey'
    )
    delivery_status = models.CharField(db_column='DeliveryStatus', max_length=50)

    class Meta:
        managed = True
        db_table = 'DeliveryStatus'
