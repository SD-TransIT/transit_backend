from rest_pandas import PandasSimpleView

from transit.reporting.average_transporter_cost_per_route import AverageTransporterCostPerRouteReport


class AverageTransporterCostPerRouteReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return AverageTransporterCostPerRouteReport(filters).create_report()
