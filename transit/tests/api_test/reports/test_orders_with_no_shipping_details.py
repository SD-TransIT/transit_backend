import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'orders_with_no_shipping_details'

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        self.complete_shipment.number_of_kilometers = None
        self.complete_shipment.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipmentNumber": self.complete_shipment.id,
            "ShipmentVolume": 200.0,
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipmentNumber": self.partially_complete_shipment.id,
            "ShipmentVolume": None,
        }])
