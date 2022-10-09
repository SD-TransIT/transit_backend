from rest_pandas import PandasSimpleView

from transit.reporting.average_product_cost_per_shipment import AverageProductCostPerShipmentReport
from transit.reporting.average_transporter_cost_per_each import AverageTransporterCostPerEachReport
from transit.reporting.percent_capacity_utilization import PercentCapacityUtilizationReport


class AverageTransporterCostPerEachReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return AverageTransporterCostPerEachReport(filters).create_report()
