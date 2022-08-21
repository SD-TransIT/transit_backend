from django.contrib.auth.models import User


MANAGE_USER_PERM = "can_manage_users"
MANAGE_FORM_PERM = 'can_manage_forms'


class UserManager(User):
    class Meta:
        proxy = True
        permissions = [(MANAGE_USER_PERM, 'Can manage users')]


class FormsClerk(User):
    class Meta:
        proxy = True
        permissions = [(MANAGE_FORM_PERM, 'Can manage forms')]
