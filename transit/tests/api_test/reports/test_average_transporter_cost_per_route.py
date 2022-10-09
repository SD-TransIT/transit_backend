import datetime

import pandas as pd
from django.test import TestCase

from transit.models import DeliveryStatus
from transit.tests.api_test.reports.utils import ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory, DeliveryStatusFactory


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'average_transporter_cost_per_route'

    def expected_payload(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRoutes": 1,
            "TotalCost": 1150.0,
            "AverageTransporterCostPerRoute": 1150.0
        }])
