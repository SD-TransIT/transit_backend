from django.urls import (
    path
)

from transit.rest_api.reports.average_product_cost_per_shipment import AverageProductCostPerShipmentReportView
from transit.rest_api.reports.average_kilometers_per_shipment_by_transporter import (
    AverageKilometersPerShipmentByTransporterReportView
)
from transit.rest_api.reports.average_transporter_cost_per_cubic_meter import \
    AverageTransporterCostPerCubicMeterReportView
from transit.rest_api.reports.average_transporter_cost_per_each import AverageTransporterCostPerEachReportView
from transit.rest_api.reports.average_transporter_cost_per_kilometer import AverageTransporterCostPerKilometerReportView
from transit.rest_api.reports.average_transporter_cost_per_route import AverageTransporterCostPerRouteReportView
from transit.rest_api.reports.number_of_dso_shipments import NumberOfDSOShipmentsReportView
from transit.rest_api.reports.percent_capacity_utilization import PercentCapacityUtilizationReportView
from transit.rest_api.reports.percent_on_time_deliveries import PercentageOnTimeDeliveriesReportView
from transit.rest_api.reports.percent_outstanding_pods import PercentageOutstandingPODsReportView

urlpatterns = [
    path(
        r'percent_capacity_utilization/',
        PercentCapacityUtilizationReportView.as_view(),
        name='percent_capacity_utilization'
    ),
    path(
        r'average_product_cost_per_shipment/',
        AverageProductCostPerShipmentReportView.as_view(),
        name='average_product_cost_per_shipment'
    ),
    path(
        r'average_transporter_cost_per_kilometer/',
        AverageTransporterCostPerKilometerReportView.as_view(),
        name='average_transporter_cost_per_kilometer'
    ),
    path(
        r'percentage_outstanding_pods/',
        PercentageOutstandingPODsReportView.as_view(),
        name='percentage_outstanding_pods'
    ),
    path(
        r'percentage_on_time_deliveries/',
        PercentageOnTimeDeliveriesReportView.as_view(),
        name='percentage_on_time_deliveries'
    ),
    path(
        r'number_of_damaged_short_over_shipments/',
        NumberOfDSOShipmentsReportView.as_view(),
        name='number_of_damaged_short_over_shipments'
    ),
    path(
        r'average_transporter_cost_per_cubic_meter/',
        AverageTransporterCostPerCubicMeterReportView.as_view(),
        name='average_transporter_cost_per_cubic_meter'
    ),
    path(
        r'average_transporter_cost_per_each/',
        AverageTransporterCostPerEachReportView.as_view(),
        name='average_transporter_cost_per_each'
    ),
    path(
        r'average_transporter_cost_per_route/',
        AverageTransporterCostPerRouteReportView.as_view(),
        name='average_transporter_cost_per_route'
    ),
    path(
        r'average_kilometers_per_shipment/',
        AverageKilometersPerShipmentByTransporterReportView.as_view(),
        name='average_kilometers_per_shipment'
    ),
]
