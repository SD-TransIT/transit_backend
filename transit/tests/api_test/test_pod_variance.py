from typing import Dict, Any

from django.test import TestCase

from transit.models import PODVariance
from transit.rest_api.forms.pod_variance import PODVarianceViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import PODVarianceFactory


class TestPODVarianceViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'pod_variance'
    _VIEW_SET = PODVarianceViewSet
    _MODEL_TYPE = PODVariance
    _TEST_SUBJECT_DATA = PODVarianceFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        'dso_type': 'PostnewDSOType',
    }
    _PATCH_REQUEST_PAYLOAD = {'dso_type': 'UpdatedDSOType'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return PODVarianceFactory().create_object(True)

    def setUp(self):
        super(TestPODVarianceViewSet, self).setUp()
        self._POST_REQUEST_PAYLOAD['shipment'] = self.test_subject.shipment.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'shipment': self.test_subject.shipment.pk, 'dso_type': 'TestDSOforPOD'
        }
