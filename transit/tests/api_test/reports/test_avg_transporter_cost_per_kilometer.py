import datetime

import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'average_transporter_cost_per_kilometer'

    def expected_payload(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "TotalCost": 1150.0,
            "TotalNumberOfKilometers": 1000.0,
            "AverageCostPerKilometer": 1.15
        }])
