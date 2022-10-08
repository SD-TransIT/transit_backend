from django.urls import (
    path
)

from transit.rest_api.reports.average_product_cost_per_shipment import AverageProductCostPerShipmentReportView
from transit.rest_api.reports.average_transporter_cost_per_kilometer import AverageTransporterCostPerKilometerReportView
from transit.rest_api.reports.percent_capacity_utilization import PercentCapacityUtilizationReportView

urlpatterns = [
    path(
        r'percent_capacity_utilization/',
        PercentCapacityUtilizationReportView.as_view(), name='percent_capacity_utilization'
    ),
    path(
        r'average_product_cost_per_shipment/',
        AverageProductCostPerShipmentReportView.as_view(), name='average_product_cost_per_shipment'
    ),
    path(
        r'average_transporter_cost_per_kilometer/',
        AverageTransporterCostPerKilometerReportView.as_view(), name='average_transporter_cost_per_kilometer'
    ),
]
