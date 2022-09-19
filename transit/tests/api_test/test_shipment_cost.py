from typing import Dict, Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from transit.models import ShipmentDetails
from transit.rest_api.forms.shipment.shipment_details_cost import ShipmentDetailsCostViewSet
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory


class ShipmentDetailsCostTestClient(ApiTestClient):
    # Has custom primary key - delivery_status_key
    _REVERSE_URL_BUILDER = {
        'without_cost': lambda url: reverse(F"API:shipment_details_cost-get-shipments-without-cost"),
        'with_cost': lambda url: reverse(F"API:shipment_details_cost-get-shipments-with-cost"),
    }

    def get_response(self, with_cost, auth_token=None, query=None, **extra):
        if query is None:
            query = {}
        self._auth(auth_token)
        if not with_cost:
            url = self._get_request_url('without_cost')
        else:
            url = self._get_request_url('with_cost')
        return self._make_request(self.factory.get, path=url, data=query, **extra)


class TestShipmentDetailsCostViewSet(ViewSetRequestTestBase, TestCase):
    _URL = 'shipment_details_cost'
    _VIEW_SET = ShipmentDetailsCostViewSet
    _TEST_SUBJECT_DATA = ShipmentDetailsFactory.default_values.copy()
    _API_HELPER_TYPE = ShipmentDetailsCostTestClient

    def setUp(self):
        super(TestShipmentDetailsCostViewSet, self).setUp()
        self.setup_helper()
        self._shipment_without_cost = \
            ShipmentDetailsFactory(custom_props={'transporter_base_cost': None}).create_object(True)
        self._shipment_with_cost = \
            ShipmentDetailsFactory(custom_props={'transporter_base_cost': "100.00"}).create_object(True)
        self._shipment_with_cost.transporter_base_cost = "120.00"
        self._shipment_with_cost.save()

    def test_get_without_cost(self):
        response = self._get_request_result(with_cost=False, shipment=self._shipment_without_cost)
        self.assertEqual(response.status_code, status.HTTP_200_OK, F"Response detail: {response.data}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self._shipment_without_cost.pk)

    def test_get_with_cost(self):
        response = self._get_request_result(with_cost=True, shipment=self._shipment_with_cost)
        self.assertEqual(response.status_code, status.HTTP_200_OK, F"Response detail: {response.data}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self._shipment_with_cost.pk)

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            field: test_value for field, test_value in self._TEST_SUBJECT_DATA.items() if isinstance(test_value, str)
        }

    def _get_request_result(self, with_cost, shipment):
        user_token = self.USER_HELPER.get_access_token()
        query = {
            'vehicle': shipment.transporter_details.pk,
            'transporter': shipment.transporter_details.transporter.pk
        }
        return self.API_HELPER.get_response(with_cost, auth_token=user_token, query=query)
