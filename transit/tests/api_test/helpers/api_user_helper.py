from django.contrib.auth.models import (
    User,
    Permission
)
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView


class UserTestHelper:
    _DEFAULT_TEST_DATA = {
        "username": 'TestUsername1',
        "is_staff": True,
        "password": '¡p35Tpas$VvÓrÐ4'
    }

    def __init__(self, **user_data):
        """
        Initializer for UserTestHelper, it's assigning parameters used latter on to create user_helper.
        At the moment given parameters are handled:
        - username
        - password
        - is_staff

        :param user_data: While parameters mentioned above have default values, they can be overridden by user_data.

        """
        self.user_data = {**self._DEFAULT_TEST_DATA, **user_data}
        self._TEST_USERNAME = self.user_data['username']
        self._TEST_PASSWORD = self.user_data['password']
        self._AUTH_PAYLOAD = {'username': self._TEST_USERNAME, 'password': self._TEST_PASSWORD}
        self.user = self._get_or_create_user()

    def _get_or_create_user(self):
        user = User.objects.filter(username=self._TEST_USERNAME).first()
        return user if user else self._create_user()

    def add_user_proxy_permissions(self, proxy_model):
        content_type = ContentType.objects.get_for_model(proxy_model, for_concrete_model=False)
        user_permissions = Permission.objects.filter(content_type=content_type)
        for permission in user_permissions:
            self.user.user_permissions.add(permission)

    def add_user_permission(self, permission_codename):
        permission = Permission.objects.get(codename=permission_codename)
        self.user.user_permissions.add(permission)

    def get_access_token(self):
        """
        Uses self._AUTH_PAYLOAD to authenticate user_helper with JWT, returns JWT token.
        :return: JWT Access Token.
        """
        factory = APIRequestFactory()
        request = factory.post('/token/', self._AUTH_PAYLOAD, format='json')
        response = TokenObtainPairView.as_view()(request)
        response_json = response.data
        return F'Bearer {response_json["access"]}'

    def _create_user(self):
        user = User(**self.user_data)
        user.set_password(self.user_data['password'])
        user.save()
        return user
