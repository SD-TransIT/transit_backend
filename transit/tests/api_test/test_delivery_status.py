from typing import Dict, Any

from django.test import TestCase

from transit.models import DeliveryStatus
from transit.rest_api.forms.delivery_status import DeliveryStatusViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import DeliveryStatusFactory


class TestDeliveryStatusViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'delivery_status'
    _VIEW_SET = DeliveryStatusViewSet
    _MODEL_TYPE = DeliveryStatus
    _TEST_SUBJECT_DATA = DeliveryStatusFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {"delivery_status_key": "not_delivered", 'delivery_status': 'Not Delivered'}
    _PATCH_REQUEST_PAYLOAD = {"delivery_status_key": "delivered", 'delivery_status': 'Delivered9'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return DeliveryStatusFactory().create_object(True)

    def setUp(self):
        super(TestDeliveryStatusViewSet, self).setUp()

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            **self._TEST_SUBJECT_DATA
        }
