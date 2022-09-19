import django_filters
from rest_framework import serializers

from transit.models import ItemDetails
from transit.rest_api.abstract import BaseModelFormViewSet


class ItemDetailsSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = ItemDetails
        fields = [
            'id', 'item', 'item_name', 'expiry_date', 'manufacturing_date',
            'received_date', 'gtin', 'batch_number', 'lot_number', 'serial_number', 'funding_source'
        ]
        read_only_fields = ['id']


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


class ItemDetailsViewSet(BaseModelFormViewSet):
    filterset_class = ItemDetailsFilter
    queryset = ItemDetails.objects.all().order_by('-id')
    search_fields = [
        'id', 'item__name', 'expiry_date', 'manufacturing_date',
        'received_date', 'gtin', 'batch_number', 'lot_number', 'serial_number',
        'funding_source'
    ]

    def get_serializer_class(self):
        return ItemDetailsSerializer
