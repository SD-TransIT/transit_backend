from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.permissions import IsFormsClerk


class BaseFormViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAuthenticated, IsFormsClerk)
