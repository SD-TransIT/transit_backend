from typing import Dict, Any

from django.test import TestCase

from transit.models import ModeOfTransport
from transit.rest_api.forms.mode_of_transport_master import ModeOfTransportViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import ModeOfTransportFactory


class TestModeOfTransportViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'mode_of_transport'
    _VIEW_SET = ModeOfTransportViewSet
    _MODEL_TYPE = ModeOfTransport
    _TEST_SUBJECT_DATA = {**ModeOfTransportFactory.default_values}

    _POST_REQUEST_PAYLOAD = {
        'class_mode': 'CustomTestClass',
        'vehicle_type': 'CustomTestVehicle'
    }
    _PATCH_REQUEST_PAYLOAD = {
        'class_mode': 'UpdatedCustomTestClass'
    }

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'class_mode': 'TestClass', 'vehicle_type': 'TestVehicle'
        }
