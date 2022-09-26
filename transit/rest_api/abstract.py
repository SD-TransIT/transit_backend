import django_filters
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.permissions import IsFormsClerk


class BaseModelFormViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    permission_classes = (IsAuthenticated, IsFormsClerk)


class BaseGenericViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsFormsClerk)


class BaseApiSetView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsFormsClerk)
