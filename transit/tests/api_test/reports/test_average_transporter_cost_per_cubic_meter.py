import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'average_transporter_cost_per_cubic_meter'

    def setUp(self):
        # Volume is required
        super(TestReportCapacity, self).setUp()
        product_item = self.partially_complete_shipment.order_mapping\
            .first().order_details.line_items.first().product
        product_item.volume = 123.0
        product_item.save()
        self.partially_complete_shipment.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.complete_shipment.ship_date.date(),
            "TransporterName": self.complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "TotalVolume": 20.0,
            "TotalCost": 1150.0,
            "AverageTransporterCostPerCubicMeter": 57.5
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.partially_complete_shipment.ship_date.date(),
            "TransporterName": self.partially_complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.partially_complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "",
            "TotalVolume": 123.0,
            "TotalCost": 0,
            "AverageTransporterCostPerCubicMeter": 0.0
        }])
