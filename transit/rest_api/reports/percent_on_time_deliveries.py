from rest_pandas import PandasSimpleView

from transit.reporting.average_product_cost_per_shipment import AverageProductCostPerShipmentReport
from transit.reporting.percent_capacity_utilization import PercentCapacityUtilizationReport
from transit.reporting.percentage_on_time_deliveries import PercentageOnTimeDeliveriesReport
from transit.reporting.percentage_outstanding_pods import PercentageOutstandingPODsReport


class PercentageOnTimeDeliveriesReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return PercentageOnTimeDeliveriesReport(filters).create_report()
