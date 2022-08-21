import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import Supplier
from transit.rest_api.manual_uploads.fields import FormsDataFields
from transit.rest_api.permissions import IsFormsClerk


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS]
        ordering = ['-id']


class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'email': ['exact', 'iexact', 'startswith'],
        }


class SupplierViewSet(viewsets.ModelViewSet):
    filterset_class = SupplierFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = Supplier.objects.all().order_by('-id')

    def get_serializer_class(self):
        return SupplierSerializer
