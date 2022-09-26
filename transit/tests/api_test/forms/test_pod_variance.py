from typing import Dict, Any

from django.test import TestCase

from transit.models import PODVariance
from transit.rest_api.forms.pod_variance import PODVarianceViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import PODVarianceFactory, OrderLineDetailsFactory


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
        self._additional_order_line_detail = OrderLineDetailsFactory().create_object(True)

        self._POST_REQUEST_PAYLOAD['shipment'] = self.test_subject.shipment.pk
        self._POST_REQUEST_PAYLOAD['pod_variance_details'] = [{
            'order_line_details': self._additional_order_line_detail.pk,
            'quantity': 17
        }]

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'shipment': self.test_subject.shipment.pk, 'dso_type': 'TestDSOforPOD'
        }

    @property
    def expected_post_obj(self):
        return self._MODEL_TYPE.objects.filter(
            shipment=self.test_subject.shipment.pk, details__quantity=17,
            details__order_line_details__id=self._additional_order_line_detail.pk
        ).first()
