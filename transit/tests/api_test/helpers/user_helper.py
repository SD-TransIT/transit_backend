from django.contrib.auth.models import (
    User,
    Permission
)
from django.contrib.contenttypes.models import ContentType


class UserTestHelper:
    _TEST_USERNAME = "TestUser"
    _TEST_PASSWORD = "TestPassword"
    _TEST_DATA_USER = {
        "username": _TEST_USERNAME,
        "is_staff": True,
        "password": _TEST_PASSWORD
    }

    def get_or_create_user(self):
        user = User.objects.filter(username=self._TEST_USERNAME).first()
        return user if user else self._create_user()

    def add_user_proxy_permissions(self, proxy_model):
        user = User.objects.filter(username=self._TEST_USERNAME).get()
        content_type = ContentType.objects.get_for_model(proxy_model, for_concrete_model=False)
        user_permissions = Permission.objects.filter(content_type=content_type)
        for permission in user_permissions:
            user.user_permissions.add(permission)

    def add_user_permission(self, permission_codename):
        user = User.objects.filter(username=self._TEST_USERNAME).get()
        permission = Permission.objects.get(codename=permission_codename)
        user.user_permissions.add(permission)

    def _create_user(self):
        user = User(**self._TEST_DATA_USER)
        user.set_password(self._TEST_DATA_USER['password'])
        user.save()
        return user
