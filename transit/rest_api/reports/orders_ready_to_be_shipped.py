from rest_pandas import PandasSimpleView

from transit.reporting.orders_ready_to_be_shipped import OrdersReadyToBeShippedReport


class OrdersReadyToBeShippedReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):

        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return OrdersReadyToBeShippedReport(filters).create_report()
