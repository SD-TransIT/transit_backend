import os
import re
import shutil
import tempfile
from typing import Dict, Any

from django.test import TestCase, override_settings
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import ShipmentDetails
from transit.rest_api.forms.shipment.shipment_details import ShipmentDetailsViewSet
from transit.rest_api.forms.shipment.shipment_files import ShipmentDetailFilesViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.api_test_client import ApiTestClient
from transit.tests.test_objects_factory import ShipmentDetailsFactory, DriverFactory, \
    TransporterDetailsFactory, SupplierFactory, DeliveryStatusFactory, OrderDetailsFactory


@override_settings(MEDIA_ROOT='transit/tests/photo_temp_files')
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
        self.__additional_order = OrderDetailsFactory().create_object(True)

        self._POST_REQUEST_PAYLOAD['transporter_details'] = self.__additional_transporter_details.pk
        self._POST_REQUEST_PAYLOAD['driver'] = self.__additional_driver.pk
        self._POST_REQUEST_PAYLOAD['supplier'] = self.__additional_supplier.pk

        self._POST_REQUEST_PAYLOAD['delivery_status'] = self.__additional_delivery_status.pk
        self._POST_REQUEST_PAYLOAD['pod_status'] = self.__additional_pod_status.pk
        self._POST_REQUEST_PAYLOAD['orders'] = [self.__additional_order.pk]

        self._PATCH_REQUEST_PAYLOAD['driver'] = self.__additional_driver.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            field: test_value for field, test_value in self._TEST_SUBJECT_DATA.items() if isinstance(test_value, str)
        }

    def test_photo_upload(self):
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b'some file text')
            tmp.seek(0)
            client = ApiTestClient('shipment_details_files', ShipmentDetailFilesViewSet)
            payload = {
                'file': tmp,
                'shipment': self.test_subject.pk,
            }
            try:
                response = client.make_post_request(
                    encode_multipart('BoUnDaRyStRiNg', payload),
                    auth_token=self.USER_HELPER.get_access_token(),
                    content_type='multipart/form-data; boundary=BoUnDaRyStRiNg'
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                response = client.make_get_request(
                    identifier=response.data['id'],
                    auth_token=self.USER_HELPER.get_access_token())

                file_url, shipment = response.data['file'], response.data['shipment']

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIsNotNone(file_url)
                self.assertEqual(shipment, self.test_subject.pk)
            finally:
                # Cleanup temporary test media root
                if os.path.exists('transit/tests/photo_temp_files'):
                    shutil.rmtree('transit/tests/photo_temp_files')

    @property
    def expected_post_obj(self):
        self._POST_REQUEST_PAYLOAD.pop('orders')
        return self._MODEL_TYPE.objects.filter(
            **self._POST_REQUEST_PAYLOAD
        ).first()
