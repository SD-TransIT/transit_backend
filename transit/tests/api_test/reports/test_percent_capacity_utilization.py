import datetime

import pandas as pd
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from transit.rest_api.excel_uploads import ItemDetailExcelUploadView
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderLineDetailsFactory


class ReportCapacityTestClient(ApiTestClient):
    _REVERSE_URL_BUILDER = {
        **ApiTestClient._REVERSE_URL_BUILDER,
        'report': lambda url: reverse(F"REPORTS:{url}"),
    }

    def get_report(self, auth_token, from_date, to_date, **extra):
        self._auth(auth_token)
        url = self._get_request_url('report')
        query = {'date_from': from_date, 'date_to': to_date, 'format': 'json'}
        return self._make_request(self.factory.get, path=url, data=query, **extra)


class TestReportCapacity(ViewSetRequestTestBase, TestCase):
    _URL = 'percent_capacity_utilization'
    _VIEW_SET = ItemDetailExcelUploadView
    _API_HELPER_TYPE = ReportCapacityTestClient

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        self.setup_helper()
        ship_date_1 = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        ship_date_2 = datetime.datetime(year=2021, month=5, day=30, tzinfo=datetime.timezone.utc)
        self.shipment = ShipmentDetailsFactory(custom_props={'ship_date': ship_date_1}).create_object(True)
        self.shipment2 = ShipmentDetailsFactory(custom_props={'ship_date': ship_date_2}).create_object(True)
        self.order_line_detail = OrderLineDetailsFactory().create_object(True)

        service = ShipmentOrdersService()
        service.add_orders_to_shipment(shipment=self.shipment, orders=[self.order_line_detail.order_details])

    def test_report_generation(self):
        token = self.USER_HELPER.get_access_token()
        response = self.API_HELPER.get_report(token, '2021-07-01', '2021-09-30')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pd.testing.assert_frame_equal(response.data, self.expected_payload())

    def expected_payload(self):
        return pd.DataFrame([{
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "VehicleCapacityVolume": 40.0,
            "volume": 20.0,
            "PercentUtilization": 50.0
        }])