from rest_pandas import PandasSimpleView

from transit.reporting.average_transporter_cost_per_cubic_meter import AverageTransporterCostPerCubicMeterReport


class AverageTransporterCostPerCubicMeterReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return AverageTransporterCostPerCubicMeterReport(filters).create_report()
