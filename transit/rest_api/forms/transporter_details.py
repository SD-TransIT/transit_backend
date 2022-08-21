import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import TransporterDetails
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.permissions import IsFormsClerk


class TransporterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransporterDetails
        fields = [
            'transporter', 'mode_of_transport', 'vehicle_number',
            'vehicle_capacity_volume', 'vehicle_capacity_weight'
        ]
        ordering = ['-id']


class TransporterDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = TransporterDetails
        fields = {
            'vehicle_number': ['exact'],
            'vehicle_capacity_volume': ['exact', 'gte', 'lte'],
            'vehicle_capacity_weight': ['exact', 'gte', 'lte'],
        }


class TransporterDetailsViewSet(BaseFormViewSet):
    filterset_class = TransporterDetailsFilter
    queryset = TransporterDetails.objects.all().order_by('-id')

    def get_serializer_class(self):
        return TransporterDetailsSerializer
