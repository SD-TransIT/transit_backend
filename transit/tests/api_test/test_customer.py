from typing import Dict, Any

from django.test import TestCase
from rest_framework.reverse import reverse

from transit.models import Customer, CustomerWeekDays
from transit.rest_api.forms.customer.customer import CustomerViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import CustomerFactory, CustomerTypeFactory


class CustomerTestClient(ApiTestClient):
    # Has custom primary key - delivery_status_key
    _REVERSE_URL_BUILDER = {
        **ApiTestClient._REVERSE_URL_BUILDER,
        'replace_working_hours': lambda url, id_: reverse(
            F"API:{url}-replace-working-hours", kwargs={'pk': id_}
        ),
    }

    def replace_working_hours(self, payload, customer, auth_token=None, **extra):
        self._auth(auth_token)
        url = self._get_request_url('replace_working_hours', id_=customer.pk)
        return self._make_request(self.factory.post, path=url, data=payload, **extra)


class TestCustomerViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'customer'
    _VIEW_SET = CustomerViewSet
    _MODEL_TYPE = Customer
    _TEST_SUBJECT_DATA = CustomerFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **CustomerFactory.default_values.copy(), 'name': 'newName'
    }
    _PATCH_REQUEST_PAYLOAD = {'name': 'updatedName', 'first_name': 'UpdatedFirstName'}

    _API_HELPER_TYPE = CustomerTestClient

    @classmethod
    def _get_or_create_test_subject(cls):
        return CustomerFactory().create_object(True)

    def setUp(self):
        super(TestCustomerViewSet, self).setUp()
        self._additional_item = CustomerTypeFactory(custom_props={"customer_type_name": "SecondTestType"})\
            .create_object(save=True)
        self._PATCH_REQUEST_PAYLOAD['customer_type'] = self._additional_item.pk

        self._POST_REQUEST_PAYLOAD['customer_type'] = self._additional_item.pk
        self._POST_REQUEST_PAYLOAD['week_days'] = [{
            'day': 1, 'opening_time': '4', 'closing_time': '1'
        }]

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            **self._TEST_SUBJECT_DATA, 'customer_type': self.test_subject.customer_type.pk,
        }

    def test_post(self):
        super(TestCustomerViewSet, self).test_post()
        self.assertTrue(CustomerWeekDays.objects.filter(
            closing_time=1, opening_time=4, closed=False
        ).exists())

    @property
    def expected_post_obj(self):
        self._POST_REQUEST_PAYLOAD.pop('week_days')
        return self._MODEL_TYPE.objects.filter(
            **self._POST_REQUEST_PAYLOAD
        ).first()

    def test_replace_working_hours(self):
        token = self.USER_HELPER.get_access_token()
        # Extend post request by additional week day data
        self._POST_REQUEST_PAYLOAD['week_days'] = [{"day": 3, "closed": True}]
        self.API_HELPER.make_post_request(
            self._POST_REQUEST_PAYLOAD, token
        )
        payload = self._build_week_days_payload()

        response = self.API_HELPER.replace_working_hours(payload, self.test_subject, token)
        delivery_hour_1_created = self.test_subject.week_days\
            .filter(closed=True, day=2, customer=self.test_subject.pk)\
            .exists()
        delivery_hour_2_created = self.test_subject.week_days\
            .filter(closed=False, opening_time="10:00", closing_time="14:00", customer=self.test_subject.pk)\
            .exists()

        self.assertEqual(self.test_subject.week_days.count(), 2)  # Only 2 new week days existing, rest removed
        self.assertTrue(delivery_hour_1_created)
        self.assertTrue(delivery_hour_2_created)

    def _build_week_days_payload(self):
        return {
            "week_days": [
                {
                    "id": 1, "customer": self.test_subject.pk,  # id and customer should be irrelevant
                    "day": 2, "closed": False,
                    "opening_time": "10:00", "closing_time": "14:00",
                },
                {
                    "day": 2, "closed": True
                }
            ]
        }
