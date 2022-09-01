from django.test import TestCase
from rest_framework import status

from transit.rest_api.avaialble_froms_meta import FormsInfoViewSet
from transit.rest_api.forms_router import manual_forms
from transit.tests.api_test.helpers.api_crud_test_case import ViewSetRequestTestBase


class TestUserViewSet(ViewSetRequestTestBase, TestCase):
    _URL = 'available_forms'
    _VIEW_SET = FormsInfoViewSet
    _USERNAME = 'FormsApiUser'

    def setUp(self):
        super(TestUserViewSet, self).setUp()
        self.setup_helper()

    def test_get_list(self):
        response = self.get_request_result()
        available_forms = [form[2] for form in manual_forms().registry]
        self.assertEqual(response.status_code, status.HTTP_200_OK, F"Response detail: {response.data}")
        labels = [form_data['label'] for form_data in response.data]
        self.assertListEqual(labels, available_forms, 'Listed forms don\'t match manual forms urls')
