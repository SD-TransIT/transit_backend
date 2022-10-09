from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryStatus(models.Model):
    class Status(models.TextChoices):  # noqa: WPS141
        UNDEFINED = 'undefined', _('Undefined')
        DELIVERED = 'delivered', _('Delivered')
        NOT_DELIVERED = 'not_delivered', _('Not Delivered')

    delivery_status_key = models.CharField(
        max_length=64, primary_key=True, unique=True,
        db_column='DeliveryStatusKey', blank=False, null=False,
    )

    delivery_status = models.CharField(
        db_column='DeliveryStatus', max_length=50,
        choices=Status.choices, default=Status.UNDEFINED
    )

    class Meta:
        managed = True
        db_table = 'DeliveryStatus'
