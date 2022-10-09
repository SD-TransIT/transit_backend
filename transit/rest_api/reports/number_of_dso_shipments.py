from rest_pandas import PandasSimpleView

from transit.reporting.average_product_cost_per_shipment import AverageProductCostPerShipmentReport
from transit.reporting.number_of_dso_shipments import NumberOfDSOShipmentsReport
from transit.reporting.percent_capacity_utilization import PercentCapacityUtilizationReport
from transit.reporting.percentage_outstanding_pods import PercentageOutstandingPODsReport


class NumberOfDSOShipmentsReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return NumberOfDSOShipmentsReport(filters).create_report()
