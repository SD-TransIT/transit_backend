from django.contrib.auth.models import User


MANAGE_USER_PERMS = "can_manage_users"


class UserManager(User):
    class Meta:
        proxy = True
        permissions = [(MANAGE_USER_PERMS, 'Can manage users')]
