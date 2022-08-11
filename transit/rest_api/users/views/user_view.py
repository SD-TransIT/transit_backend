from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.permissions import IsUserManager
from transit.rest_api.users.serializers import (
    UserSerializer,
    UserUpdateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsUserManager)
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserUpdateSerializer if self.request.method == 'PUT' else UserSerializer
