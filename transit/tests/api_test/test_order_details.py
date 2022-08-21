from typing import Dict, Any

from django.test import TestCase
from rest_framework import status

from transit.models import OrderDetails
from transit.rest_api.forms.order_details import OrderDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import OrderDetailsFactory, OrderLineDetailsFactory, \
    CustomerFactory


class TestOrderDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'order_details'
    _VIEW_SET = OrderDetailsViewSet
    _MODEL_TYPE = OrderDetails
    _TEST_SUBJECT_DATA = OrderDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **OrderDetailsFactory.default_values.copy(), 'order_received_date': '2022-08-18',
    }
    _PATCH_REQUEST_PAYLOAD = {
        'order_received_date': '2022-08-18'
    }

    @classmethod
    def _get_or_create_test_subject(cls):
        return OrderDetailsFactory().create_object(True)

    def setUp(self):
        super(TestOrderDetailsViewSet, self).setUp()
        self._order_list_detail = \
            OrderLineDetailsFactory(custom_props={"order_details": self.test_subject}).create_object(save=True)
        self._additional_customer = CustomerFactory(custom_props={
            'name': 'NewTestCustomer', 'customer_type__customer_type_name': 'NewUniqueNameTest'
        }).create_object(save=True)
        self._POST_REQUEST_PAYLOAD['line_items'] = [{
            'product': int(self._order_list_detail.product.pk),
            'item_details': int(self._order_list_detail.item_details.pk),
            'quantity': 10,
        }]
        self._POST_REQUEST_PAYLOAD['customer'] = self._additional_customer.pk
        self._PATCH_REQUEST_PAYLOAD['customer'] = self._additional_customer.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {}

    @property
    def expected_post_obj(self):
        return self._MODEL_TYPE.objects.filter(
            order_received_date=self._POST_REQUEST_PAYLOAD['order_received_date'],
            line_items__product__pk=self._order_list_detail.product.pk
        ).first()

    def test_update_line_details_forbidden(self):
        copy = self._PATCH_REQUEST_PAYLOAD.copy()
        self._PATCH_REQUEST_PAYLOAD = {'order_received_date': '1970-01-01', 'line_items': [{
            'product': self._order_list_detail.product.pk,
            'item_details': self._order_list_detail.item_details.pk,
            'quantity': 10,
        }]}
        response = self.patch_request_result()
        self._PATCH_REQUEST_PAYLOAD = copy
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated = self._MODEL_TYPE.objects.filter(order_received_date='1970-01-01').first()
        self.assertIsNone(updated)
