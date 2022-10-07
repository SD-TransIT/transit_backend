import datetime

from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import ItemDetails
from transit.rest_api.excel.excel_uploads import ItemDetailExcelUploadView
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.test_objects_factory import ItemFactory


class TestItemDetailsExcelUpload(ViewSetRequestTestBase, TestCase):
    _URL = 'item_detail_excel_upload'
    _VIEW_SET = ItemDetailExcelUploadView
    _ENCODE_MULTIPART = 'BoUnDaRyStRiNg'
    _EXCEL_FILE_PATH = 'transit/tests/api_test/excel_upload/test_excel_files/ItemDetailTestExcel.xlsx'

    def setUp(self):
        super(TestItemDetailsExcelUpload, self).setUp()
        self.setup_helper()

    def test_item_details_upload(self):
        # Setup for excel references
        self._test_item_1 = ItemFactory(custom_props={'name': 'Test Item 1'}).create_object()
        self._test_item_2 = ItemFactory(custom_props={'name': 'Test Item 2'}).create_object()

        response = self._sent_excel_file()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(ItemDetails.objects.filter(
            item__name='Test Item 1', batch_number='BN001',
            expiry_date=datetime.date(year=2023, month=12, day=31),
            manufacturing_date=datetime.date(year=2021, month=2, day=1),
            received_date=datetime.date(year=2022, month=10, day=12),
            lot_number='lotnumber', serial_number='12367', gtin=12345,
            funding_source='Test Source 1'
        ).exists())
        self.assertTrue(ItemDetails.objects.filter(
            item__name='Test Item 2', batch_number='BN002'
        ).exists())

    def _sent_excel_file(self):
        with open(self._EXCEL_FILE_PATH, 'rb') as tmp:
            payload = {'file': tmp}
            return self.API_HELPER.make_post_request(
                encode_multipart(self._ENCODE_MULTIPART, payload),
                auth_token=self.USER_HELPER.get_access_token(),
                content_type=F'multipart/form-data; boundary={self._ENCODE_MULTIPART}'
            )
