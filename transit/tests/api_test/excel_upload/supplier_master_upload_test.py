import datetime

from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import Supplier
from transit.rest_api.excel_uploads import ItemMasterExcelUploadView, ItemDetailExcelUploadView
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase


class TestSupplierMasterExcelUpload(ViewSetRequestTestBase, TestCase):
    _URL = 'supplier_master_excel_upload'
    _VIEW_SET = ItemDetailExcelUploadView
    _ENCODE_MULTIPART = 'BoUnDaRyStRiNg'
    _EXCEL_FILE_PATH = 'transit/tests/api_test/excel_upload/test_excel_files/SupplierMasterTestExcel.xlsx'

    def setUp(self):
        super(TestSupplierMasterExcelUpload, self).setUp()
        self.setup_helper()

    def test_supplier_master_upload(self):
        response = self._sent_excel_file()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Supplier.objects.filter(
            name='SUPPLIER1',
            phone='9123912',
            email='email@email.email',
            address_1='Ad1', address_2='Ad2', address_3='Ad3',
            city='City1', state='State1', country='Country1',
            latitude_longitude='latlong',
        ).exists())
        self.assertTrue(Supplier.objects.filter(name='SUPPLIER2').exists())

    def _sent_excel_file(self):
        with open(self._EXCEL_FILE_PATH, 'rb') as tmp:
            payload = {'file': tmp}
            return self.API_HELPER.make_post_request(
                encode_multipart(self._ENCODE_MULTIPART, payload),
                auth_token=self.USER_HELPER.get_access_token(),
                content_type=F'multipart/form-data; boundary={self._ENCODE_MULTIPART}'
            )
