from decimal import Decimal

from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import Item
from transit.rest_api.excel.excel_uploads import ItemMasterExcelUploadView
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase


class TestItemMasterExcelUpload(ViewSetRequestTestBase, TestCase):
    _URL = 'item_master_excel_upload'
    _VIEW_SET = ItemMasterExcelUploadView
    _ENCODE_MULTIPART = 'BoUnDaRyStRiNg'
    _EXCEL_FILE_PATH = 'transit/tests/api_test/excel_upload/test_excel_files/ItemMasterTestExcel.xlsx'

    def setUp(self):
        super(TestItemMasterExcelUpload, self).setUp()
        self.setup_helper()

    def test_item_master_upload(self):
        response = self._sent_excel_file()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Item.objects.filter(
            name='Test Item 1', category='CAT1', sub_category='SUBCAT1',
            volume=10.0, weight=11, cost=21, conditions=Item.Condition.COLD_CHAIN).exists())
        self.assertTrue(Item.objects.filter(
            name='Test Item 2', category='cat2', cost=Decimal('3.14'),
            conditions=Item.Condition.UNKNOWN))
        self.assertTrue(Item.objects.filter(
            name='Test Item 3', sub_category='SUBCAT3', volume=9999,
            conditions=Item.Condition.AMBIENT).exists())

    def _sent_excel_file(self):
        with open(self._EXCEL_FILE_PATH, 'rb') as tmp:
            payload = {'file': tmp}
            return self.API_HELPER.make_post_request(
                encode_multipart(self._ENCODE_MULTIPART, payload),
                auth_token=self.USER_HELPER.get_access_token(),
                content_type=F'multipart/form-data; boundary={self._ENCODE_MULTIPART}'
            )
