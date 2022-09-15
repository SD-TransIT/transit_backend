from typing import Dict, Any

from django.test import TestCase

from transit.models import Supplier
from transit.rest_api.forms.supplier_master import SupplierViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import SupplierFactory


class TestSupplierViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'supplier'
    _VIEW_SET = SupplierViewSet
    _MODEL_TYPE = Supplier

    _TEST_SUBJECT_DATA = SupplierFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {**SupplierFactory.default_values.copy(), 'name': 'TestSupplierNew'}
    _PATCH_REQUEST_PAYLOAD = {**SupplierFactory.default_values.copy(), 'name': 'TestSupplierUpdated'}

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return self._TEST_SUBJECT_DATA
