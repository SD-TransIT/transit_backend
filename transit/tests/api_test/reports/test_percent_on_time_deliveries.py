import datetime

import pandas as pd
from django.test import TestCase
from rest_framework import status

from transit.models import DeliveryStatus
from transit.rest_api.excel.excel_uploads import ItemDetailExcelUploadView
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.reports.utils import ReportTestClient, ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderLineDetailsFactory, DeliveryStatusFactory


class TestReportOnTimeDeliveries(ReportTestCaseMixin, TestCase):
    _URL = 'percentage_on_time_deliveries'

    def setUp(self):
        super(TestReportOnTimeDeliveries, self).setUp()
        ship_date_3 = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        delivery_expected = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        delivery = delivery_expected + datetime.timedelta(days=10)
        self.shipment3 = ShipmentDetailsFactory(custom_props={
            'ship_date': ship_date_3,
            'expected_delivery_date': delivery_expected,
            'delivery_date': delivery,
            'delay_justified': True,
            'transporter_details': self.shipment.transporter_details
        }).create_object(True)

    def expected_payload(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "Shipments": 2,
            "TotalOnTimeDeliveries": 1,
            "TotalJustifiedDelayedDeliveries": 1,
            "PercentageOfOnTimeDeliveries": 50.0,
            "PercentageOfJustifiedDelayedDeliveries": 50.0,
        }])
