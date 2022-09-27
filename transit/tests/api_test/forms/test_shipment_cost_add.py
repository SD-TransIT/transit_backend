from typing import Dict, Any

from django.test import TestCase
from django.urls import reverse

from transit.models import ShipmentDetails
from transit.rest_api.forms.shipment.shipment_details import ShipmentDetailsViewSet
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory


class ShipmentCostAddTestClient(ApiTestClient):
    _REVERSE_URL_BUILDER = {
        'add_costs_to_shipment': lambda url: reverse(F"API:{url}-add-costs-to-shipment"),
    }

    def add_costs_to_shipment(self, payload, auth_token=None, **extra):
        self._auth(auth_token)
        url = self._get_request_url('add_costs_to_shipment')
        return self._make_request(self.factory.put, path=url, data=payload, **extra)


class TestShipmentCostAddViewSet(ViewSetRequestTestBase, TestCase):
    _URL = 'cost'
    _VIEW_SET = ShipmentDetailsViewSet
    _MODEL_TYPE = ShipmentDetails
    _TEST_SUBJECT_DATA = ShipmentDetailsFactory.default_values.copy()
    _API_HELPER_TYPE = ShipmentCostAddTestClient

    @classmethod
    def _get_or_create_test_subject(cls):
        return ShipmentDetailsFactory().create_object(True)

    def setUp(self):
        super(TestShipmentCostAddViewSet, self).setUp()
        self.setup_helper()
        self._shipment_cost = \
            ShipmentDetailsFactory(custom_props={'transporter_base_cost': None}).create_object(True)

    def test_add_costs_to_shipment(self):
        token = self.USER_HELPER.get_access_token()

        payload = self._build_add_costs_to_shipment_payload(self._shipment_cost.pk)
        self.API_HELPER.add_costs_to_shipment(payload, token)

        is_shipment_updated_by_cost = self._MODEL_TYPE.objects\
            .filter(
              id=self._shipment_cost.pk,
              transporter_base_cost='0.65',
              transporter_additional_cost='2.66',
              number_of_kilometers='678.00'
            )\
            .exists()

        self.assertTrue(is_shipment_updated_by_cost)

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            field: test_value for field, test_value in self._TEST_SUBJECT_DATA.items() if isinstance(test_value, str)
        }

    def _build_add_costs_to_shipment_payload(self, shipment_pk):
        return [
                {
                    "id": shipment_pk,
                    "transporter_base_cost": "0.65",
                    "transporter_additional_cost": "2.66",
                    "number_of_kilometers": "678",
                },
            ]
