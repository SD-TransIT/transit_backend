import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import OrderDetails, OrderLineDetails
from transit.rest_api.permissions import IsFormsClerk


class OrderLineDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = OrderLineDetails
        fields = {
            'quantity': ['exact', 'lte', 'gte'],
            'old_quantity': ['exact', 'lte', 'gte']
        }


class OrderDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = OrderDetails
        fields = {
            'order_received_date': ['exact', 'lte', 'gte'],
        }


class OrderLineDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineDetails
        fields = ['product', 'item_details', 'quantity', 'old_quantity']
        ordering = ['-id']


class OrderDetailsSerializer(serializers.ModelSerializer):
    filterset_class = OrderDetailsFilter
    line_items = OrderLineDetailsSerializer(many=True, required=False)

    class Meta:
        model = OrderDetails
        fields = ['line_items', 'customer', 'order_received_date']
        ordering = ['-id']

    def create(self, validated_data):
        line_items = validated_data.pop('line_items', [])
        order = OrderDetails.objects.create(**validated_data)
        for item_dict in line_items:
            item_dict['order_details'] = order
            OrderLineDetails(**item_dict).save()
        return order  # noqa: R504

    def validate(self, data): # noqa: WPS-122
        """
        Update of line items directly through OrderDetails is forbidden.
        """
        validated = super(OrderDetailsSerializer, self).validate(data)
        if self.instance and validated.get('line_items'):
            raise serializers.ValidationError(
                _("Order Line Details have to be updated using order_line_details endpoint.")
            )
        return validated


class OrderDetailsViewSet(viewsets.ModelViewSet):
    filterset_class = OrderDetailsFilter
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = OrderDetails.objects.all().order_by('-order_received_date')

    def get_serializer_class(self):
        return OrderDetailsSerializer


class OrderLineDetailsViewSet(viewsets.ModelViewSet):
    filterset_class = OrderLineDetailsFilter
    # Optional ID required by creating through OrderDetails
    id = serializers.IntegerField(required=False)
    lookup_url_kwarg = 'pk'
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = OrderLineDetails.objects.all()

    def get_serializer_class(self):
        return OrderLineDetailsSerializer
