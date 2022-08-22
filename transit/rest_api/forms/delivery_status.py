import django_filters
from rest_framework import serializers

from transit.models import DeliveryStatus
from transit.rest_api.abstract import BaseFormViewSet


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


class DeliveryStatusViewSet(BaseFormViewSet):
    filterset_class = DeliveryStatusFilter
    queryset = DeliveryStatus.objects.all().order_by('delivery_status')

    def get_serializer_class(self):
        return DeliveryStatusSerializer
