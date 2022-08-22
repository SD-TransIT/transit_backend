from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.permissions import IsFormsClerk


class BaseFormViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsFormsClerk)
