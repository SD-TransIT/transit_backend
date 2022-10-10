import datetime

import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory


class TestReportOnTimeDeliveries(ReportTestCaseMixin, TestCase):
    _URL = 'percentage_on_time_deliveries'

    def setUp(self):
        super(TestReportOnTimeDeliveries, self).setUp()
        ship_date_3 = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        delivery_expected = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        delivery = delivery_expected + datetime.timedelta(days=10)
        self.complete_shipment = ShipmentDetailsFactory(custom_props={
            'ship_date': ship_date_3,
            'expected_delivery_date': delivery_expected,
            'delivery_date': delivery,
            'delay_justified': True,
            'transporter_details': self.complete_shipment.transporter_details
        }).create_object(True)

        self.partially_complete_shipment.delivery_date = delivery
        self.partially_complete_shipment.expected_delivery_date = delivery_expected
        self.partially_complete_shipment.save()

    def expected_payload_complete(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.complete_shipment.ship_date.date(),
            "TransporterName": self.complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "Shipments": 2,
            "TotalOnTimeDeliveries": 1,
            "TotalJustifiedDelayedDeliveries": 1,
            "PercentageOfOnTimeDeliveries": 50.0,
            "PercentageOfJustifiedDelayedDeliveries": 50.0,
        }])

    def expected_payload_partial(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": self.partially_complete_shipment.ship_date.date(),
            "TransporterName": self.partially_complete_shipment.transporter_details.transporter.name,
            "VehicleNumber": self.partially_complete_shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "",
            "Shipments": 1,
            "TotalOnTimeDeliveries": 0,
            "TotalJustifiedDelayedDeliveries": 1,
            "PercentageOfOnTimeDeliveries": 0.0,
            "PercentageOfJustifiedDelayedDeliveries": 100.0,
        }])
