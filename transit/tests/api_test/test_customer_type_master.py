from typing import Dict, Any

from django.test import TestCase

from transit.models import CustomerType
from transit.rest_api.manual_uploads.customer_type_master import CustomerTypeViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin


class TestCustomerTypeViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'customer_type'
    _VIEW_SET = CustomerTypeViewSet
    _MODEL_TYPE = CustomerType

    _TEST_SUBJECT_DATA = {'customer_type_name': 'CustomerTypeNameBase'}
    _POST_REQUEST_PAYLOAD = {'customer_type_name': 'CustomerTypeNameBaseNew'}
    _PATCH_REQUEST_PAYLOAD = {'customer_type_name': 'CustomerTypeNameUpdated'}

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return self._TEST_SUBJECT_DATA
