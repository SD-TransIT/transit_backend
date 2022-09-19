from typing import Dict, Any, Collection

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from transit.models import OrderDetails, ShipmentDetails
from transit.rest_api.forms.shipment.shipment_details_cost import ShipmentDetailsCostViewSet
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderDetailsFactory


class ShipmentDetailsOrdersClient(ApiTestClient):
    # Has custom primary key - delivery_status_key
    _REVERSE_URL_BUILDER = {
        'add_orders': lambda url, _id: reverse(F"API:{url}-add-orders-to-shipment",  kwargs={'pk': _id}),
        'remove_orders': lambda url, _id: reverse(F"API:{url}-remove-orders-from-shipment",  kwargs={'pk': _id}),
        'replace_orders': lambda url, _id: reverse(F"API:{url}-replace-orders-in-shipment",  kwargs={'pk': _id}),
    }

    def make_orders_post(self, payload, action, shipment, auth_token=None, **extra):
        self._auth(auth_token)
        url = self._get_request_url(action, _id=shipment.pk)
        return self._make_request(self.factory.post, path=url, data=payload, **extra)


class TestShipmentDetailsCostViewSet(ViewSetRequestTestBase, TestCase):
    _URL = 'shipment_details_orders'
    _VIEW_SET = ShipmentDetailsCostViewSet
    _TEST_SUBJECT_DATA = ShipmentDetailsFactory.default_values.copy()
    _API_HELPER_TYPE = ShipmentDetailsOrdersClient

    def setUp(self):
        super(TestShipmentDetailsCostViewSet, self).setUp()
        self.setup_helper()
        self._new_order: OrderDetails = OrderDetailsFactory().create_object(True)
        self._new_shipment: ShipmentDetails = ShipmentDetailsFactory().create_object(True)
        self._user_token = self.USER_HELPER.get_access_token()

    def test_add_order(self):
        payload = self._build_order_payload([self._new_order])
        response = self.API_HELPER.make_orders_post(payload, 'add_orders', self._new_shipment, self._user_token)
        self._assert_added_orders(response)

    def _assert_added_orders(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response_order = response.data[0]['order']
        self.assertEqual(response_order, self._new_order.order_details_id)
        self.assertEqual(self._new_order, self._new_shipment.order_mapping.get().order_details)

    def test_replace_order(self):
        payload = self._build_order_payload([self._new_order])
        response = self.API_HELPER.make_orders_post(payload, 'replace_orders', self._new_shipment, self._user_token)
        self._assert_added_orders(response)

    def test_remove_order(self):
        payload = self._build_order_payload([self._new_order])
        self.API_HELPER.make_orders_post(payload, 'add_orders', self._new_shipment, self._user_token)
        response = self.API_HELPER.make_orders_post(payload, 'remove_orders', self._new_shipment, self._user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(self._new_shipment.order_mapping.all().count(), 0)

    def _build_order_payload(self, orders: Collection[OrderDetails]):
        return {"orders": [order.order_details_id for order in orders]}
