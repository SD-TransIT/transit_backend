import django_filters
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from transit.models import OrderDetails, OrderLineDetails
from transit.rest_api.abstract import BaseModelFormViewSet
from transit.rest_api.forms.order_details.order_line_details import OrderLineDetailsSerializer
from transit.services.order_service import OrderLineItemsService


class OrderDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = OrderDetails
        fields = {
            'order_received_date': ['exact', 'lte', 'gte'],
        }


class OrderDetailsOrderLineDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    batch_number = serializers.CharField(source='item_details.batch_number', read_only=True)

    class Meta:
        model = OrderLineDetails
        fields = [
            'id', 'product', 'item_details', 'quantity', 'old_quantity', 'product_name', 'batch_number'
        ]
        read_only_fields = ['id']
        ordering = ['-id']


class OrderLineDetailsSerializerWrapper(serializers.Serializer):
    """
    Utilizes CustomerWeekDaysSerializer for purpose of bulk replacement of working hours.
    """
    _service = OrderLineItemsService()

    line_items = serializers.ListField(
        child=OrderDetailsOrderLineDetailsSerializer(), required=True, allow_empty=True
    )

    def update(self, instance, validated_data):
        raise NotImplementedError('update() not supported,'
                                  ' data should be alternated using replace_working_hours')

    def create(self, validated_data):
        raise NotImplementedError('create() not supported,'
                                  ' data should be alternated using replace_working_hours')

    def replace_line_items(self):
        line_items = [OrderLineDetails(**day) for day in self.validated_data['line_items']]
        self._service.replace_order_line_items(order=self.instance, line_items=line_items)

    def to_representation(self, instance):
        field = self.fields['line_items']
        return field.to_representation(instance.line_items.all())


class OrderDetailsSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    line_items = OrderDetailsOrderLineDetailsSerializer(many=True, required=False)

    class Meta:
        model = OrderDetails
        fields = ['order_details_id', 'line_items', 'customer', 'order_received_date', 'customer_name']
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


class OrderDetailsViewSet(BaseModelFormViewSet):
    filterset_class = OrderDetailsFilter
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    queryset = OrderDetails.objects.all().order_by('-order_received_date')
    search_fields = ['order_details_id', 'customer__name', 'customer__id', 'order_received_date']

    _line_items_serializer = OrderLineDetailsSerializerWrapper

    def get_serializer_class(self):
        return OrderDetailsSerializer

    @swagger_auto_schema(methods=['post'], request_body=OrderLineDetailsSerializerWrapper)
    @action(detail=True, methods=['post'])
    def replace_line_items(self, request, pk=None):
        serializer = self._build_details_serializer(request)
        serializer.replace_line_items()
        return self._valid_items(serializer)

    def _build_details_serializer(self, request):
        order = self.get_object()
        serializer = self._line_items_serializer(instance=order, data=request.data)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        return serializer

    def _valid_items(self, serializer):
        return Response(serializer.to_representation(self.get_object()), status=status.HTTP_200_OK)
