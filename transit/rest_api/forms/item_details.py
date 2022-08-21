import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import ItemDetails
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.permissions import IsFormsClerk


class ItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemDetails
        fields = [
            'item', 'expiry_date', 'manufacturing_date',
            'received_date', 'gtin', 'batch_number', 'lot_number', 'serial_number', 'funding_source'
        ]


class ItemDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = ItemDetails
        fields = {
            'expiry_date': ['gte', 'lte', 'iexact'],
            'manufacturing_date': ['gte', 'lte', 'iexact'],
            'batch_number': ['exact', 'iexact', 'startswith'],
            'serial_number': ['exact', 'iexact', 'startswith']
        }
        ordering = ['-id']


class ItemDetailsViewSet(BaseFormViewSet):
    filterset_class = ItemDetailsFilter
    queryset = ItemDetails.objects.all().order_by('-id')

    def get_serializer_class(self):
        return ItemDetailsSerializer
