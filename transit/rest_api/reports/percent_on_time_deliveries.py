from rest_pandas import PandasSimpleView

from transit.reporting.percentage_on_time_deliveries import PercentageOnTimeDeliveriesReport


class PercentageOnTimeDeliveriesReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return PercentageOnTimeDeliveriesReport(filters).create_report()
