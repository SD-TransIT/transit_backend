from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework import status

from transit.models import Customer
from transit.rest_api.excel.excel_uploads import ItemDetailExcelUploadView
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.test_objects_factory import CustomerTypeFactory


class TestCustomerMasterExcelUpload(ViewSetRequestTestBase, TestCase):
    _URL = 'customer_detail_excel_upload'
    _VIEW_SET = ItemDetailExcelUploadView
    _ENCODE_MULTIPART = 'BoUnDaRyStRiNg'
    _EXCEL_FILE_PATH = 'transit/tests/api_test/excel_upload/test_excel_files/CustomerMasterTestExcel.xlsx'

    def setUp(self):
        super(TestCustomerMasterExcelUpload, self).setUp()
        self.setup_helper()

    def test_client_master_upload(self):
        CustomerTypeFactory(custom_props={"customer_type_name": "TYPE1"}) \
            .create_object(save=True)
        response = self._sent_excel_file()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Customer.objects.filter(
            name='CLIENT1', first_name='John', last_name='Doe',
            phone='9123912',
            email='email@email.email',
            address_1='Ad1', address_2='Ad2', address_3='Ad3',
            city='City1', state='State1', country='Country1',
            latitude_longitude='latlong',
            customer_type__customer_type_name='TYPE1'
        ).exists())
        self.assertTrue(Customer.objects.filter(name='CLIENT2').exists())

    def _sent_excel_file(self):
        with open(self._EXCEL_FILE_PATH, 'rb') as tmp:
            payload = {'file': tmp}
            return self.API_HELPER.make_post_request(
                encode_multipart(self._ENCODE_MULTIPART, payload),
                auth_token=self.USER_HELPER.get_access_token(),
                content_type=F'multipart/form-data; boundary={self._ENCODE_MULTIPART}'
            )
