from typing import Dict, Any

from django.test import TestCase

from transit.models import ShipmentDetails
from transit.rest_api.manual_uploads.shipment import ShipmentDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import ShipmentDetailsFactory, DriverFactory, \
    TransporterDetailsFactory, SupplierFactory, DeliveryStatusFactory


class TestShipmentDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'shipment_details'
    _VIEW_SET = ShipmentDetailsViewSet
    _MODEL_TYPE = ShipmentDetails
    _TEST_SUBJECT_DATA = ShipmentDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **ShipmentDetailsFactory.default_values.copy(),
    }
    _PATCH_REQUEST_PAYLOAD = {'transporter_base_cost': '1200.00'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return ShipmentDetailsFactory().create_object(True)

    def setUp(self):
        super(TestShipmentDetailsViewSet, self).setUp()

        self.__additional_supplier = SupplierFactory().create_object(True)
        self.__additional_transporter_details = TransporterDetailsFactory().create_object(True)
        self.__additional_driver = DriverFactory(
            custom_props={'transporter': self.__additional_transporter_details.transporter}
        ).create_object(True)
        self.__additional_delivery_status = DeliveryStatusFactory(
            custom_props={'delivery_status_key': 'delivered4', 'delivery_status': 'Delivered4'}
        ).create_object(True)
        self.__additional_pod_status = DeliveryStatusFactory().create_object(True)

        self._POST_REQUEST_PAYLOAD['transporter_details'] = self.__additional_transporter_details.pk
        self._POST_REQUEST_PAYLOAD['driver'] = self.__additional_driver.pk
        self._POST_REQUEST_PAYLOAD['supplier'] = self.__additional_supplier.pk
        self._POST_REQUEST_PAYLOAD['delivery_status'] = self.__additional_delivery_status.pk
        self._POST_REQUEST_PAYLOAD['pod_status'] = self.__additional_pod_status.pk

        self._PATCH_REQUEST_PAYLOAD['driver'] = self.__additional_driver.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            field: test_value for field, test_value in self._TEST_SUBJECT_DATA.items() if isinstance(test_value, str)
        }
