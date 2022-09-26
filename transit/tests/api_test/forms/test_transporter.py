from typing import Dict, Any

from django.test import TestCase

from transit.models import Transporter
from transit.rest_api.forms.transporter import TransporterViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import TransporterFactory


class TestTransporterViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'transporter'
    _VIEW_SET = TransporterViewSet
    _MODEL_TYPE = Transporter

    _TEST_SUBJECT_DATA = TransporterFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **TransporterFactory.default_values.copy(), 'name': 'TestTransporterNew', 'city': 'TransporterCity2'}
    _PATCH_REQUEST_PAYLOAD = {'name': 'UpdatedTransporterTest', 'city': 'UpdatedCity'}

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return self._TEST_SUBJECT_DATA
