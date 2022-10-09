import pandas as pd
from django.test import TestCase

from transit.models import PODVariance
from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'number_of_damaged_short_over_shipments'

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        PODVariance.objects.create(shipment=self.complete_shipment, dso_type=PODVariance.DSOType.DAMAGED.name)
        PODVariance.objects.create(shipment=self.partially_complete_shipment, dso_type=PODVariance.DSOType.DAMAGED.name)

        self.order_line_detail_complete.old_quantity = 5.0
        self.order_line_detail_complete.save()

        self.order_line_detail_partial.old_quantity = 3.0
        self.order_line_detail_partial.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.complete_shipment.ship_date.date(),
            "TransporterName": self.complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "DSOType": 'DAMAGED',
            "OldQuantity": 5.0,
            "NewQuantity": 10.0,
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.partially_complete_shipment.ship_date.date(),
            "TransporterName": self.partially_complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.partially_complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "",
            "DSOType": 'DAMAGED',
            "OldQuantity": 3.0,
            "NewQuantity": 5.0,
        }])
