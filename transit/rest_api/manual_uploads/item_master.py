import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import Item
from transit.rest_api.permissions import IsFormsClerk


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'volume', 'cost', 'weight', 'category', 'sub_category', 'conditions']


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


class ItemViewSet(viewsets.ModelViewSet):
    filterset_class = ItemFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = Item.objects.all().order_by('-id')

    def get_serializer_class(self):
        return ItemSerializer
