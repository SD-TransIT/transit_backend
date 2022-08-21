from rest_framework.permissions import BasePermission

from transit.models.user_proxy import (
    UserManager,
    MANAGE_USER_PERM,
)


class IsUserManager(BasePermission):
    """
       Permission allowing access for users that have been assigned the 'can_manage_users' permission
    """
    def has_permission(self, request, view):
        return request.user.has_perm(f'{UserManager._meta.app_label}.{MANAGE_USER_PERM}')


class IsFormsClerk(BasePermission):
    """
       Permission allowing access CRUD operations on Upload Forms and Excel Uploads.
    """
    def has_permission(self, request, view):
        return request.user.has_perm('transit.can_manage_forms')
