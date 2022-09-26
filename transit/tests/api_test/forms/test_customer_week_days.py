from typing import Dict, Any

from django.test import TestCase

from transit.models import CustomerWeekDays
from transit.rest_api.forms.customer.week_days import CustomerWeekDaysViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import CustomerWeekDaysFactory, CustomerFactory


class TestCustomerWeekDaysViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'customer_week_days'
    _VIEW_SET = CustomerWeekDaysViewSet
    _MODEL_TYPE = CustomerWeekDays
    _TEST_SUBJECT_DATA = CustomerWeekDaysFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **CustomerWeekDaysFactory.default_values.copy(), 'opening_time': '7',
        'closing_time': '15'
    }
    _PATCH_REQUEST_PAYLOAD = {
        'closing_time': '19'
    }

    @classmethod
    def _get_or_create_test_subject(cls):
        return CustomerWeekDaysFactory().create_object(True)

    def setUp(self):
        super(TestCustomerWeekDaysViewSet, self).setUp()
        self._customer = CustomerFactory(custom_props={
            'name': 'NewTestCustomer', 'customer_type__customer_type_name': 'NewUniqueNameTest'
        }).create_object(save=True)
        self._POST_REQUEST_PAYLOAD['customer'] = int(self._customer.pk)

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'customer': self.test_subject.customer.pk, 'closing_time': '18', 'opening_time': '10', 'closed': False
        }
