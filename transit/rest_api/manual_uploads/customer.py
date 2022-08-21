import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import Customer
from transit.rest_api.manual_uploads.fields import FormsDataFields
from transit.rest_api.permissions import IsFormsClerk


class CustomerSerializer(serializers.ModelSerializer):
    filterset_fields = ['name', 'first_name', 'last_name', 'phone', 'email', 'customer_type']

    class Meta:
        model = Customer
        fields = [
            *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS,
            'name', 'first_name', 'last_name', 'phone', 'email', 'customer_type'
        ]
        ordering = ['-id']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'first_name': ['exact', 'iexact', 'startswith'],
            'last_name': ['exact', 'iexact', 'startswith'],
        }


class CustomerViewSet(viewsets.ModelViewSet):
    filterset_class = CustomerFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = Customer.objects.all().order_by('-id')

    def get_serializer_class(self):
        return CustomerSerializer
