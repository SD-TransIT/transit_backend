from typing import Dict, Any

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from transit.models import OrderDetails
from transit.rest_api.forms.order_details import OrderDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import OrderDetailsFactory, OrderLineDetailsFactory, \
    CustomerFactory


class OrderLineItemsTestClient(ApiTestClient):
    _REVERSE_URL_BUILDER = {
        **ApiTestClient._REVERSE_URL_BUILDER,
        'replace_line_items': lambda url, id_: reverse(
            F"API:{url}-replace-line-items", kwargs={'pk': id_}
        ),
    }

    def replace_line_items(self, payload, order, auth_token=None, **extra):
        self._auth(auth_token)
        url = self._get_request_url('replace_line_items', id_=order.pk)
        return self._make_request(self.factory.post, path=url, data=payload, **extra)


class TestOrderDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'order_details'
    _VIEW_SET = OrderDetailsViewSet
    _MODEL_TYPE = OrderDetails
    _TEST_SUBJECT_DATA = OrderDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **OrderDetailsFactory.default_values.copy(), 'order_received_date': '2022-08-18',
        'order_details_id': 'UniqueNewCharDetailID'
    }
    _PATCH_REQUEST_PAYLOAD = {
        'order_received_date': '2022-08-18'
    }
    _API_HELPER_TYPE = OrderLineItemsTestClient

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
        return {
            **self._TEST_SUBJECT_DATA
        }

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

    def test_replace_working_hours(self):
        token = self.USER_HELPER.get_access_token()
        # Extend post request by additional week day data
        self.API_HELPER.make_post_request(
            self._POST_REQUEST_PAYLOAD, token
        )

        payload = {
            'line_items': [{
                'product': self._order_list_detail.product.pk,
                'item_details': self._order_list_detail.item_details.pk,
                'quantity': 12
            }]
        }

        self.API_HELPER.replace_line_items(payload, self.test_subject, token)

        self.assertEqual(self.test_subject.line_items.count(), 1)

        # New exists
        self.assertTrue(self.test_subject.line_items
                        .filter(quantity=12, order_details=self.test_subject.pk).exists())

        # Old one removed
        self.assertFalse(self.test_subject.line_items
                         .filter(quantity=10, order_details=self.test_subject.pk).exists())
