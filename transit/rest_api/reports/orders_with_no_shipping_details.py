from rest_pandas import PandasSimpleView

from transit.reporting.orders_with_no_shipping_details import OrdersWithNoShippingDetailsReport
from transit.reporting.percentage_outstanding_pods import PercentageOutstandingPODsReport


class OrdersWithNoShippingDetailsReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return OrdersWithNoShippingDetailsReport(filters).create_report()
