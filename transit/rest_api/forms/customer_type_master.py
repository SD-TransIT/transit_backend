import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import CustomerType
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.permissions import IsFormsClerk


class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = ['customer_type_name']
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

    def get_serializer_class(self):
        return CustomerTypeSerializer
