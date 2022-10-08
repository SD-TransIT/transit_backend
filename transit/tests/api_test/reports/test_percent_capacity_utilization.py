import datetime

import pandas as pd
from django.test import TestCase
from rest_framework import status

from transit.rest_api.excel.excel_uploads import ItemDetailExcelUploadView
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.reports.utils import ReportTestClient, ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderLineDetailsFactory


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'percent_capacity_utilization'

    def expected_payload(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "VehicleCapacityVolume": 40.0,
            "volume": 20.0,
            "PercentUtilization": 50.0
        }])
