import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'average_transporter_cost_per_each'

    def setUp(self):
        # Invoiced (with cost) shipments only
        super(TestReportCapacity, self).setUp()
        self.partially_complete_shipment.transporter_base_cost = 123.0
        self.partially_complete_shipment.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.complete_shipment.ship_date.date(),
            "TransporterName": self.complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "TotalEaches": 10.0,
            "TotalCost": 1150.0,
            "AverageTransporterCostPerEach": 115.0
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.partially_complete_shipment.ship_date.date(),
            "TransporterName": self.partially_complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.partially_complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "",
            "TotalEaches": 5.0,
            "TotalCost": 123.0,
            "AverageTransporterCostPerEach": 24.6
        }])
