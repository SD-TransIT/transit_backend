from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryStatus(models.Model):
    class Status(models.TextChoices):  # noqa: WPS141
        UNDEFINED = 'undefined', _('Undefined')
        DELIVERED = 'delivered', _('Delivered')
        NOT_DELIVERED = 'not_delivered', _('Not Delivered')
        OTHER = 'other', _('Other')
        POD_SIGNED_COMPLETE = 'pod_signed_complete', _("POD signed complete")
        POD_SIGNED_DSO = 'pod_signed_dso', _('POD signed DSO')
        ROBBERY = 'robbery', _('Robbery')
        ACCIDENT = 'accident', _('Accident')

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
