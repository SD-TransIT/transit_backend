from rest_pandas import PandasSimpleView

from transit.reporting.average_kilometers_per_shipment_by_transporter import (
    AverageKilometersPerShipmentByTransporterReport
)


class AverageKilometersPerShipmentByTransporterReportView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        filters = {
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to')}
        return AverageKilometersPerShipmentByTransporterReport(filters).create_report()
