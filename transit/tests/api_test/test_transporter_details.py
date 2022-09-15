from typing import Dict, Any

from django.test import TestCase

from transit.models import TransporterDetails
from transit.rest_api.forms.transporter_details import TransporterDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import TransporterDetailsFactory, TransporterFactory, \
    ModeOfTransportFactory


class TestTransporterDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'transporter_details'
    _VIEW_SET = TransporterDetailsViewSet
    _MODEL_TYPE = TransporterDetails
    _TEST_SUBJECT_DATA = TransporterDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **TransporterDetailsFactory.default_values.copy(), 'vehicle_number': '21954',
    }
    _PATCH_REQUEST_PAYLOAD = {'vehicle_capacity_volume': '120', 'vehicle_capacity_weight': '800'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return TransporterDetailsFactory().create_object(True)

    def setUp(self):
        super(TestTransporterDetailsViewSet, self).setUp()
        self._additional_transporter = \
            TransporterFactory(custom_props={"name": "SecondTransporter"}).create_object(save=True)
        self._PATCH_REQUEST_PAYLOAD['transporter'] = self._additional_transporter.pk
        self._POST_REQUEST_PAYLOAD['transporter'] = self._additional_transporter.pk
        self._additional_mode = \
            ModeOfTransportFactory(custom_props={"class_mode": "NewTestMode"}).create_object(save=True)
        self._PATCH_REQUEST_PAYLOAD['mode_of_transport'] = self._additional_mode.pk
        self._POST_REQUEST_PAYLOAD['mode_of_transport'] = self._additional_mode.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'transporter': self.test_subject.transporter.pk,
            'vehicle_number': '75192', 'vehicle_capacity_volume': '40', 'vehicle_capacity_weight': '70'
        }
