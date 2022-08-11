from rest_framework import status

from transit.rest_api.authentication.jwt_views import DecoratedTokenObtainPairView
from transit.tests.api_test import ApiTest


class ApiLoginTest(ApiTest):
    def setUp(self):
        super(ApiLoginTest, self).setUp()
        self.payload = None

    def get_view(self):
        return DecoratedTokenObtainPairView

    def test_post_token_success(self):
        self.payload = {'username': self._TEST_USERNAME, 'password': self._TEST_PASSWORD}
        response = self.make_post_request('/token/', self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_token_bad_request_error(self):
        # Create an instance of a POST request.
        response = self.make_post_request('/token/', self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_token_unauthorized_error(self):
        self.payload = {'username': f'{self._TEST_USERNAME}sss', 'password': self._TEST_PASSWORD}
        response = self.make_post_request('/token/', self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
