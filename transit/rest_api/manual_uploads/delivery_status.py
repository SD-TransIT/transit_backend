import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import DeliveryStatus
from transit.rest_api.permissions import IsUserManager


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


class DeliveryStatusViewSet(viewsets.ModelViewSet):
    filterset_class = DeliveryStatusFilter
    permission_classes = (IsAuthenticated, IsUserManager)
    queryset = DeliveryStatus.objects.all().order_by('delivery_status')

    def get_serializer_class(self):
        return DeliveryStatusSerializer
