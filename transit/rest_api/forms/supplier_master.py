import django_filters
from rest_framework import serializers

from transit.models import Supplier
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.forms.fields import FormsDataFields


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'email', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS]
        read_only_fields = ['id']
        ordering = ['-id']


class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'email': ['exact', 'iexact', 'startswith'],
        }


class SupplierViewSet(BaseFormViewSet):
    filterset_class = SupplierFilter
    queryset = Supplier.objects.all().order_by('-id')

    def get_serializer_class(self):
        return SupplierSerializer
