from django.contrib.auth.models import User
from rest_framework import status

from transit.models.user_proxy import MANAGE_USER_PERMS
from transit.rest_api.urls import UserViewSet
from transit.tests.api_test import ApiTest


class ApiLoginTest(ApiTest):
    _URL = '/users/'
    _TEST_NEW_USER_USERNAME = 'newuser'
    _TEST_NEW_USER_PASSWORD = 'newuserpass'

    def setUp(self):
        super(ApiLoginTest, self).setUp()
        self.payload = {
            'username': self._TEST_NEW_USER_USERNAME,
            'password': self._TEST_NEW_USER_PASSWORD,
            'is_staff': True
        }
        self.auth_payload = {'username': self._TEST_USERNAME, 'password': self._TEST_PASSWORD}

    def get_view(self):
        return UserViewSet

    def test_post_create_user_without_token(self):
        response = self.make_post_request(self._URL, self.payload, self._POST_ACTION)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create_user_without_proper_user_perms(self):
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_post_request(self._URL, self.payload, self._POST_ACTION)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_create_user_with_proper_user_perms(self):
        self.add_user_permission(MANAGE_USER_PERMS)
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_post_request(self._URL, self.payload, self._POST_ACTION)
        new_user = User.objects.filter(username=self._TEST_NEW_USER_USERNAME).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(new_user)
        if new_user:
            self.assertEqual(new_user.username, self._TEST_NEW_USER_USERNAME)

    def test_get_users_without_token(self):
        response = self.make_get_request(self._URL, self.payload, self._GET_ACTION)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_without_proper_user_perms(self):
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_get_request(self._URL, self.payload, self._GET_ACTION)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_with_proper_user_perms(self):
        self.add_user_permission(MANAGE_USER_PERMS)
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_get_request(self._URL, self.payload, self._GET_ACTION)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_users_without_token(self):
        response = self.make_put_request(f'{self._URL}{self.user.pk}/', self.payload, self.user.pk, self._PUT_ACTION)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_users_without_proper_user_perms(self):
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_put_request(f'{self._URL}{self.user.pk}/', self.payload, self.user.pk, self._PUT_ACTION)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_with_proper_user_perms(self):
        self.add_user_permission(MANAGE_USER_PERMS)
        self.header = self.get_authorize_header(self.auth_payload)
        self.payload.pop('is_staff'), self.payload.pop('password')
        response = self.make_put_request(f'{self._URL}{self.user.pk}/', self.payload, self.user.pk, self._PUT_ACTION)
        updated_user = User.objects.filter(username=self._TEST_NEW_USER_USERNAME).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(updated_user)
        if updated_user:
            self.assertEqual(updated_user.username, self._TEST_NEW_USER_USERNAME)

    def test_delete_users_without_token(self):
        response = self.make_delete_request(f'{self._URL}{self.user.pk}/', self.user.pk, self._DELETE_ACTION)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_users_without_proper_user_perms(self):
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_delete_request(f'{self._URL}{self.user.pk}/', self.user.pk, self._DELETE_ACTION)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_proper_user_perms(self):
        self.add_user_permission(MANAGE_USER_PERMS)
        self.header = self.get_authorize_header(self.auth_payload)
        response = self.make_delete_request(f'{self._URL}{self.user.pk}/', self.user.pk, self._DELETE_ACTION)
        updated_user = User.objects.filter(username=self._TEST_USERNAME).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(updated_user)
