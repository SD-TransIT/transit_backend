import django_filters
from rest_framework import serializers

from transit.models import TransporterDetails
from transit.rest_api.abstract import BaseFormViewSet


class TransporterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransporterDetails
        fields = [
            'id', 'transporter', 'mode_of_transport', 'vehicle_number',
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
