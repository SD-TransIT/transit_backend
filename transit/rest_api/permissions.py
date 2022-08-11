from rest_framework.permissions import BasePermission

from transit.models.user_proxy import (
    UserManager,
    MANAGE_USER_PERMS,
)


class IsUserManager(BasePermission):
    """
       Allows user to manage users
    """

    def has_permission(self, request, view):
        return request.user.has_perm(f'{UserManager._meta.app_label}.{MANAGE_USER_PERMS}')
