from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from transit.models.user_proxy import MANAGE_USER_PERM
from transit.rest_api.urls import UserViewSet
from transit.tests.api_test.helpers import UserTestHelper
from transit.tests.api_test.helpers.api_test_client import ApiTestClient


class ApiUserTest(TestCase):

    _URL = 'users'
    _VIEW_SET = UserViewSet
    _TEST_NEW_USER_USERNAME = 'newuser'
    _TEST_NEW_USER_PASSWORD = 'newuserpass'
    _TEST_PAYLOAD = {
        'username': _TEST_NEW_USER_USERNAME,
        'password': _TEST_NEW_USER_PASSWORD,
        'is_staff': True
    }

    def setUp(self):
        super(ApiUserTest, self).setUp()
        self.payload = self._TEST_PAYLOAD
        self.API_HELPER = ApiTestClient(self._URL, self._VIEW_SET)
        user_helper_valid = UserTestHelper(username='ApiAdminUser')
        user_helper_valid.add_user_permission(MANAGE_USER_PERM)
        self.USER_HELPER_VALID = user_helper_valid
        self.USER_HELPER_INVALID = UserTestHelper(username='ApiRegularUser')
        self.USER_HELPER_OTHER = UserTestHelper(username='ApiUnrelatedUser')

    def test_post_create_user_without_token(self):
        response = self.API_HELPER.make_post_request(self.payload, None)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create_user_without_proper_user_perms(self):
        user = self.USER_HELPER_INVALID.get_access_token()
        response = self.API_HELPER.make_post_request(self.payload, user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_create_user_with_proper_user_perms(self):
        user = self.USER_HELPER_VALID.get_access_token()
        response = self.API_HELPER.make_post_request(self.payload, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.filter(username=self._TEST_NEW_USER_USERNAME).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_user.username, self._TEST_NEW_USER_USERNAME)

    def test_get_users_without_token(self):
        response = self.API_HELPER.make_get_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_without_proper_user_perms(self):
        user = self.USER_HELPER_INVALID.get_access_token()
        response = self.API_HELPER.make_get_request(auth_token=user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_with_proper_user_perms(self):
        user = self.USER_HELPER_VALID.get_access_token()
        response = self.API_HELPER.make_get_request(auth_token=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_users_without_token(self):
        self._run_update_test(None, status.HTTP_401_UNAUTHORIZED)

    def test_update_users_without_proper_user_perms(self):
        user = self.USER_HELPER_INVALID.get_access_token()
        self._run_update_test(user, status.HTTP_403_FORBIDDEN)

    def _additional_check(self, response):
        updated_user = User.objects.filter(username=self.USER_HELPER_OTHER.user.username).first()
        self.assertIsNotNone(updated_user)

    def test_update_user_with_proper_user_perms(self):
        user = self.USER_HELPER_VALID.get_access_token()
        self._run_update_test(user, status.HTTP_200_OK, self._additional_check)

    def test_delete_users_without_token(self):
        self._run_delete_test(None, status.HTTP_401_UNAUTHORIZED)

    def test_delete_users_without_proper_user_perms(self):
        user = self.USER_HELPER_INVALID.get_access_token()
        self._run_delete_test(user, status.HTTP_403_FORBIDDEN)

    def _delete_additional_check(self, response):
        exists = User.objects.filter(username=self.payload['username']).exists()
        self.assertFalse(exists)

    def test_delete_user_with_proper_user_perms(self):
        user = self.USER_HELPER_VALID.get_access_token()
        self._run_delete_test(user, status.HTTP_204_NO_CONTENT, self._delete_additional_check)

    def _run_delete_test(self, user_token, expected_status, additional_check=None):
        delete_user = self.USER_HELPER_OTHER.user
        response = self.API_HELPER.make_delete_request(delete_user.pk, auth_token=user_token)
        self.assertEqual(response.status_code, expected_status)
        if additional_check:
            additional_check(response)

    def _run_update_test(self, user_token, expected_status, additional_check=None):
        updated_user = UserTestHelper(username='new_user1').user
        payload = {"username": "new_user2"}
        response = self.API_HELPER.make_patch_request(
            payload=payload, identifier=updated_user.pk, auth_token=user_token)
        self.assertEqual(response.status_code, expected_status)
        if additional_check:
            additional_check(response)
