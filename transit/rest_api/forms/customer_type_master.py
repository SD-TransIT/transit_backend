import django_filters
from rest_framework import serializers, filters

from transit.models import CustomerType
from transit.rest_api.abstract import BaseFormViewSet


class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = ['id', 'customer_type_name']
        read_only_fields = ['id']
        ordering = ['-id']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerType
        fields = {
            'customer_type_name': ['exact', 'iexact', 'startswith']
        }


class CustomerTypeViewSet(BaseFormViewSet):
    filterset_class = CustomerFilter
    queryset = CustomerType.objects.all().order_by('-id')
    search_fields = ['id', 'customer_type_name']

    def get_serializer_class(self):
        return CustomerTypeSerializer
