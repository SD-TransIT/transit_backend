import django_filters
from rest_framework import serializers

from transit.models import DeliveryStatus
from transit.rest_api.abstract import BaseModelFormViewSet


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'


class DeliveryStatusFilter(django_filters.FilterSet):
    class Meta:
        model = DeliveryStatus
        fields = {
            'delivery_status': ['exact', 'iexact', 'startswith']
        }
        ordering = ['-id']


class DeliveryStatusViewSet(BaseModelFormViewSet):
    filterset_class = DeliveryStatusFilter
    queryset = DeliveryStatus.objects.all().order_by('delivery_status')
    search_fields = ['delivery_status_key', 'delivery_status']

    def get_serializer_class(self):
        return DeliveryStatusSerializer
