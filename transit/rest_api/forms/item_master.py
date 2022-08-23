import django_filters
from rest_framework import serializers

from transit.models import Item
from transit.rest_api.abstract import BaseFormViewSet


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'volume', 'cost', 'weight', 'category', 'sub_category', 'conditions']
        read_only_fields = ['id']


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'volume': ['exact', 'gte', 'lte'],
            'cost': ['exact', 'gte', 'lte'],
            'weight': ['exact', 'gte', 'lte'],
            'conditions': ['iexact', 'gte', 'lte']
        }
        ordering = ['-id']


class ItemViewSet(BaseFormViewSet):
    filterset_class = ItemFilter
    queryset = Item.objects.all().order_by('-id')

    def get_serializer_class(self):
        return ItemSerializer
