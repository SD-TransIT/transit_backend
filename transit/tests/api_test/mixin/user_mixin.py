from django.contrib.auth.models import (
    User,
    Permission
)
from django.contrib.contenttypes.models import ContentType

from transit.models import UserManager


class UserMixin:
    _TEST_USERNAME = "TestUser"
    _TEST_PASSWORD = "TestPassword"
    _TEST_DATA_USER = {
        "username": _TEST_USERNAME,
        "is_staff": True,
        "password": _TEST_PASSWORD
    }

    def get_or_create_user(self):
        user = User.objects.filter(username=self._TEST_USERNAME).first()
        if user is None:
            return self.__create_user()
        return user

    def add_permissions_to_manage_users(self):
        user = User.objects.filter(username=self._TEST_USERNAME).first()
        if user:
            content_type = ContentType.objects.get_for_model(UserManager, for_concrete_model=False)
            user_permissions = Permission.objects.filter(content_type=content_type)
            for permission in user_permissions:
                user.user_permissions.add(permission)

    def __create_user(self):
        user = User(**self._TEST_DATA_USER)
        user.set_password(self._TEST_DATA_USER['password'])
        user.save()
        return user
