from rest_pandas import PandasSimpleView

from transit.reporting.percent_capacity_utilization import PercentCapacityUtilizationReport


class PercentCapacityUtilizationReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):

        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return PercentCapacityUtilizationReport(filters).create_report()
