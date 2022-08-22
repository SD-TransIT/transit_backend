import django_filters
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.permissions import IsUserManager
from transit.rest_api.users.serializers import (
    UserSerializer,
    UserUpdateSerializer
)


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = {
            'username': ['exact', 'iexact', 'startswith'],
            'email': ['exact', 'iexact', 'startswith'],
        }


class UserViewSet(viewsets.ModelViewSet):
    filterset_class = UserFilter
    permission_classes = (IsAuthenticated, IsUserManager)
    queryset = User.objects.all().order_by('-id')

    def get_serializer_class(self):
        return UserUpdateSerializer if self.request.method in ('PUT', 'PATCH') else UserSerializer
