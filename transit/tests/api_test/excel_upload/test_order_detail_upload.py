from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import OrderDetails
from transit.rest_api.excel.excel_uploads import OrderDetailsExcelUploadView
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.test_objects_factory import ItemFactory, CustomerFactory


class TestOrderDetailExcelUpload(ViewSetRequestTestBase, TestCase):
    _URL = 'order_detail_excel_upload'
    _VIEW_SET = OrderDetailsExcelUploadView
    _ENCODE_MULTIPART = 'BoUnDaRyStRiNg'
    _EXCEL_FILE_PATH = 'transit/tests/api_test/excel_upload/test_excel_files/OrderDetailTestExcel.xlsx'

    def setUp(self):
        super(TestOrderDetailExcelUpload, self).setUp()
        self.setup_helper()

    def test_order_detail_upload(self):
        item_1 = ItemFactory(custom_props={"name": "ITEM 1"}).create_object()
        item_2 = ItemFactory(custom_props={"name": "ITEM 2"}).create_object()
        customer_1 = CustomerFactory(custom_props={"name": "CUSTOMER 1"}).create_object()
        customer_2 = CustomerFactory(custom_props={"name": "CUSTOMER 2", "customer_type": customer_1.customer_type})\
            .create_object()
        response = self._sent_excel_file()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Order received date is a string, not date.
        order_1 = OrderDetails.objects.filter(
            customer__name="CUSTOMER 1",
            order_received_date='2022-04-01 00:00:00',
        ).first()
        order_2 = OrderDetails.objects.filter(
            customer=customer_2,
            order_received_date='2022-05-30 00:00:00',
        ).first()
        self.assertIsNotNone(order_1, 'Order 1 not created from excel file')
        self.assertIsNotNone(order_2, 'Order 2 not created from excel file')
        line_items_1 = order_1.line_items.all()
        line_items_2 = order_2.line_items.all()
        self.assertEqual(line_items_1.count(), 2)
        self.assertTrue(line_items_1.filter(product=item_1, quantity=2).exists())
        self.assertTrue(line_items_1.filter(product=item_2, quantity=1).exists())
        self.assertEqual(line_items_2.count(), 1)
        self.assertTrue(line_items_2.filter(product=item_1, quantity=3).exists())

    def _sent_excel_file(self):
        with open(self._EXCEL_FILE_PATH, 'rb') as tmp:
            payload = {'file': tmp}
            return self.API_HELPER.make_post_request(
                encode_multipart(self._ENCODE_MULTIPART, payload),
                auth_token=self.USER_HELPER.get_access_token(),
                content_type=F'multipart/form-data; boundary={self._ENCODE_MULTIPART}'
            )
