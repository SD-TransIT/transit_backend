import abc
import datetime

import pandas as pd
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.reverse import reverse

from transit.models import ShipmentDetails, OrderLineDetails, ItemDetails, OrderDetails, Item
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderLineDetailsFactory


class ReportTestClient(ApiTestClient):
    _REVERSE_URL_BUILDER = {
        **ApiTestClient._REVERSE_URL_BUILDER,
        'report': lambda url: reverse(F"REPORTS:{url}"),
    }

    def get_report(self, auth_token, from_date, to_date, **extra):
        self._auth(auth_token)
        url = self._get_request_url('report')
        query = {'date_from': from_date, 'date_to': to_date, 'format': 'json'}
        return self._make_request(self.factory.get, path=url, data=query, **extra)


class ReportTestCaseMixin(abc.ABC, ViewSetRequestTestBase):
    """
    Base class for testing reports. Creates test shipments with orders.
    """
    _API_HELPER_TYPE = ReportTestClient

    def setUp(self):
        super(ReportTestCaseMixin, self).setUp()
        self.setup_helper()
        self._create_complete_shipment()
        self._create_partial_shipment()

    def test_report_generation_complete_data(self):
        """
        Report for valid data.
        """
        token = self.USER_HELPER.get_access_token()
        response = self.API_HELPER.get_report(token, '2021-07-01', '2021-09-30')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pd.testing.assert_frame_equal(response.data, self.expected_payload_complete())

    def test_report_for_no_filled_data(self):
        """
        Report for time period in which there's no shipments.
        """
        expected_error = ".*No data for report for provided filters:.*"
        with self.assertRaisesRegex(ValidationError, expected_error):
            token = self.USER_HELPER.get_access_token()
            self.API_HELPER.get_report(token, '2022-07-01', '2021-09-30')

    def test_report_for_partial_data(self):
        """
        Report for minimal correct data (e.g. shipment with only mandatory fields, no orders, etc.)
        """
        token = self.USER_HELPER.get_access_token()
        response = self.API_HELPER.get_report(token, '2021-05-01', '2021-06-02')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pd.testing.assert_frame_equal(response.data, self.expected_payload_partial())

    @abc.abstractmethod
    def expected_payload_complete(self):
        ...

    @abc.abstractmethod
    def expected_payload_partial(self):
        ...

    def _create_complete_shipment(self):
        ship_date = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        self.complete_shipment = ShipmentDetailsFactory(
            custom_props={'ship_date': ship_date, 'transporter_details__vehicle_number': None}
        ).create_object(True)
        self.order_line_detail_complete = OrderLineDetailsFactory().create_object(True)
        service = ShipmentOrdersService()
        service.add_orders_to_shipment(
            shipment=self.complete_shipment,
            orders=[self.order_line_detail_complete.order_details]
        )

    def _create_partial_shipment(self):
        ship_date = datetime.datetime(year=2021, month=5, day=30, tzinfo=datetime.timezone.utc)
        self.partially_complete_shipment = ShipmentDetails(
            transporter_details=self.complete_shipment.transporter_details,
            driver=self.complete_shipment.driver,
            supplier=self.complete_shipment.supplier,
            ship_date=ship_date,
            delivery_status=self.complete_shipment.delivery_status,
            pod_status=self.complete_shipment.pod_status,

        )
        self.partially_complete_shipment.save()

        test_item = Item()
        test_item.save()

        item_detail = ItemDetails(batch_number='AOSUDB', item=test_item)
        item_detail.save()

        order = OrderDetails(customer=self.order_line_detail_complete.order_details.customer)
        order.save()

        self.order_line_detail_partial = OrderLineDetails(
            order_details=order, product=test_item, item_details=item_detail, quantity=5
        )
        self.order_line_detail_partial.save()

        service = ShipmentOrdersService()
        service.add_orders_to_shipment(
            shipment=self.partially_complete_shipment,
            orders=[self.order_line_detail_partial.order_details]
        )
