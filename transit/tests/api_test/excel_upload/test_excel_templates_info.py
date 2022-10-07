import pandas as pd

from django.test import TestCase
from rest_framework import status

from transit.rest_api.excel.excel_templates_info import (
    ExcelTemplatesInfo,
    ExcelTemplatesInfoViewSet,
)
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase
from transit.tests.api_test.helpers.api_test_client import ApiTestClient


class ExcelTemplatesInfoFormTestClient(ApiTestClient):
    def get_excel_template(self, auth_token, form_type, **extra):
        self._auth(auth_token)
        query = {'form_type': form_type}
        return self._make_request(self.factory.get, path='/api/download_excel_template/', data=query, **extra)


class TestExcelTemplatesInfoForm(ViewSetRequestTestBase, TestCase):
    _URL = 'download_excel_template'
    _VIEW_SET = ExcelTemplatesInfoViewSet
    _API_HELPER_TYPE = ExcelTemplatesInfoFormTestClient
    _FORM_TYPE = 'customer_master'

    def setUp(self):
        super(TestExcelTemplatesInfoForm, self).setUp()
        self.setup_helper()

    def test_customer_master_download_template(self):
        token = self.USER_HELPER.get_access_token()
        response = self.API_HELPER.get_excel_template(token, self._FORM_TYPE)
        received_data_frame = pd.read_excel(response.content, na_filter=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pd.testing.assert_frame_equal(received_data_frame, self.expected_payload(self._FORM_TYPE))

    def test_customer_master_download_bad_template(self):
        token = self.USER_HELPER.get_access_token()
        response = self.API_HELPER.get_excel_template(token, 'customer_details_master')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def expected_payload(self, form_type):
        return pd.DataFrame(ExcelTemplatesInfo().excel_example_data[form_type])
