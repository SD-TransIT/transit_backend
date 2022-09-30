from django.db import models

from transit.models.base import BaseModel
from transit.models.order_details import OrderLineDetails
from transit.models.shipment import ShipmentDetails


class PODVariance(BaseModel):
    shipment = models.ForeignKey(ShipmentDetails, models.DO_NOTHING, db_column='ShipmentID',
                                 related_name='pod_variances')
    dso_type = models.CharField(
        db_column='DSOType', max_length=255, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = 'PODVariance'


class PODVarianceDetails(BaseModel):
    pod_variance = models.ForeignKey(PODVariance, models.DO_NOTHING, db_column='PODVarianceID', related_name='details')
    order_line_details = models.ForeignKey(OrderLineDetails, models.DO_NOTHING, db_column='OrderLineDetailsID')

    quantity = models.DecimalField(db_column='Quantity', max_digits=18, decimal_places=2)

    @property
    def product_name(self):
        """get product name saved in order line details"""
        return self.order_line_details.product.name

    @property
    def old_quantity(self):
        """get original quantity saved in order line details"""
        return self.order_line_details.quantity

    class Meta:
        managed = True
        db_table = 'PODVarianceDetails'
