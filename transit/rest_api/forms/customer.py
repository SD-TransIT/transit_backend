import django_filters
from rest_framework import serializers

from transit.models import Customer
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.forms.fields import FormsDataFields


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS,
            'name', 'first_name', 'last_name', 'phone', 'email', 'customer_type'
        ]
        read_only_fields = ['id']
        ordering = ['-id']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'first_name': ['exact', 'iexact', 'startswith'],
            'last_name': ['exact', 'iexact', 'startswith'],
        }


class CustomerViewSet(BaseFormViewSet):
    filterset_class = CustomerFilter
    queryset = Customer.objects.all().order_by('-id')

    def get_serializer_class(self):
        return CustomerSerializer
