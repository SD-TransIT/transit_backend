from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from transit.tests.api_test.helpers import UserTestHelper
from transit.tests.api_test.helpers.api_test_client import TokenApiTestClient


class ApiLoginTest(TestCase):
    _URL = 'token_obtain_pair'

    def setUp(self):
        super(ApiLoginTest, self).setUp()
        self.API_HELPER = TokenApiTestClient(self._URL, TokenObtainPairView)
        self.USER_HELPER = UserTestHelper(username='JWTLoginTestUser')
        self.payload = None

    def test_post_token_success(self):
        payload = self.USER_HELPER._AUTH_PAYLOAD
        response = self.API_HELPER.make_post_request(payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_token_bad_request_error(self):
        response = self.API_HELPER.make_post_request(None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_token_unauthorized_error(self):
        self.payload = {'username': 'UnknownLogin', 'password': self.USER_HELPER._TEST_PASSWORD}
        response = self.API_HELPER.make_post_request(self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
