import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from transit.models import OrderDetails, OrderLineDetails
from transit.rest_api.abstract import BaseFormViewSet


class OrderLineDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = OrderLineDetails
        fields = {
            'quantity': ['exact', 'lte', 'gte'],
            'old_quantity': ['exact', 'lte', 'gte']
        }


class OrderLineDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    batch_number = serializers.CharField(source='item_details.batch_number', read_only=True)

    class Meta:
        model = OrderLineDetails
        fields = [
            'id', 'order_details', 'product', 'item_details',
            'quantity', 'old_quantity', 'product_name', 'batch_number'
        ]
        read_only_fields = ['id']
        ordering = ['-id']


class OrderLineDetailsViewSet(BaseFormViewSet):
    filterset_class = OrderLineDetailsFilter
    # Optional ID required by creating through OrderDetails
    id = serializers.IntegerField(required=False)
    lookup_url_kwarg = 'pk'
    queryset = OrderLineDetails.objects.all()

    def get_serializer_class(self):
        return OrderLineDetailsSerializer
