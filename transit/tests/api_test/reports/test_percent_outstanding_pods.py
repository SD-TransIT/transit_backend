import datetime

import pandas as pd
from django.test import TestCase

from transit.models import DeliveryStatus
from transit.tests.api_test.reports.utils import ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory, DeliveryStatusFactory


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'percentage_outstanding_pods'

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        ship_date_3 = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        self.shipment3 = ShipmentDetailsFactory(custom_props={'ship_date': ship_date_3}).create_object(True)
        self.delivered = DeliveryStatusFactory(
            custom_props={'delivery_status_key': 'delivered', 'delivery_status': DeliveryStatus.Status.DELIVERED}
        ).create_object()
        self.shipment3.delivery_status = self.delivered
        self.shipment3.save()
        self.partially_complete_shipment.delivery_status = self.delivered
        self.partially_complete_shipment.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.complete_shipment.ship_date.date(),
            "TransporterName": self.complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": '75192',  # Default vehicle number from factory
            "CustomRouteNumber": "66",
            "TotalPODs": 1,
            "OutstandingPODs": 1,
            "PercentageOfOutstandingPODs": 100.0
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.partially_complete_shipment.ship_date.date(),
            "TransporterName": self.partially_complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": '',
            "CustomRouteNumber": "",
            "TotalPODs": 1,
            "OutstandingPODs": 1,
            "PercentageOfOutstandingPODs": 100.0
        }])
