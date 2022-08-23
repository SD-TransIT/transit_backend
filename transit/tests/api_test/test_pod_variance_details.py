from typing import Dict, Any

from django.test import TestCase

from transit.models import PODVarianceDetails
from transit.rest_api.forms.pod_variance import PODVarianceDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import PODVarianceFactory, OrderLineDetailsFactory, \
    PODVarianceDetailsFactory


class TestPODVarianceDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'pod_variance_details'
    _VIEW_SET = PODVarianceDetailsViewSet
    _MODEL_TYPE = PODVarianceDetails
    _TEST_SUBJECT_DATA = PODVarianceDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        'quantity': '400',
    }
    _PATCH_REQUEST_PAYLOAD = {'quantity': '700'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return PODVarianceDetailsFactory().create_object(True)

    def setUp(self):
        super(TestPODVarianceDetailsViewSet, self).setUp()
        self._additional_order_line_details = OrderLineDetailsFactory(
            custom_props={'order_details__customer__customer_type__customer_type_name': 'NewCustomer'}).create_object(True)
        self._additional_pod_variance = PODVarianceFactory().create_object(True)

        self._POST_REQUEST_PAYLOAD['pod_variance'] = self._additional_pod_variance.pk
        self._POST_REQUEST_PAYLOAD['order_line_details'] = self._additional_order_line_details.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'order_line_details': self.test_subject.order_line_details.pk,
            'id': self.test_subject.id,
            'quantity': '15.00'
        }

    @property
    def expected_post_obj(self):
        return self._MODEL_TYPE.objects.filter(
            pod_variance=self._additional_pod_variance.pk,
            quantity=self._POST_REQUEST_PAYLOAD['quantity'],
            order_line_details=self._additional_order_line_details.pk
        ).first()
