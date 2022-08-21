from typing import Dict, Any

from django.test import TestCase

from transit.models import Customer
from transit.rest_api.forms.customer import CustomerViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import CustomerFactory, CustomerTypeFactory


class TestCustomerViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'customer'
    _VIEW_SET = CustomerViewSet
    _MODEL_TYPE = Customer
    _TEST_SUBJECT_DATA = CustomerFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **CustomerFactory.default_values.copy(), 'name': 'newName'
    }
    _PATCH_REQUEST_PAYLOAD = {'name': 'updatedName', 'first_name': 'UpdatedFirstName'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return CustomerFactory().create_object(True)

    def setUp(self):
        super(TestCustomerViewSet, self).setUp()
        self._additional_item = CustomerTypeFactory(custom_props={"customer_type_name": "SecondTestType"})\
            .create_object(save=True)
        self._PATCH_REQUEST_PAYLOAD['customer_type'] = self._additional_item.pk
        self._POST_REQUEST_PAYLOAD['customer_type'] = self._additional_item.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            **self._TEST_SUBJECT_DATA, 'customer_type': self.test_subject.customer_type.pk,
        }
