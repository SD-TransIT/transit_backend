import django_filters

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from transit.models import TransporterDetails
from transit.rest_api.abstract import BaseModelFormViewSet


class TransporterDetailsSerializer(serializers.ModelSerializer):
    transport_name = serializers.CharField(source='transporter.name', read_only=True)
    vehicle_type = serializers.CharField(source='mode_of_transport.vehicle_type', read_only=True)

    class Meta:
        model = TransporterDetails
        fields = [
            'id', 'transporter', 'mode_of_transport', 'vehicle_number',
            'vehicle_capacity_volume', 'vehicle_capacity_weight', 'transport_name', 'vehicle_type'
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


class TransporterDetailsViewSet(BaseModelFormViewSet):
    filterset_class = TransporterDetailsFilter
    queryset = TransporterDetails.objects.all().order_by('-id')
    search_fields = [
        'id', 'transporter__name', 'vehicle_number', 'vehicle_capacity_volume',
        'vehicle_capacity_weight', 'mode_of_transport__vehicle_type'
    ]

    @action(detail=False, methods=['get'])
    def vehicles_without_pagination(self, request, pk=None):
        transporter = self.request.query_params.get('transporter', '')
        queryset = self.queryset
        if transporter:
            queryset = queryset.filter(transporter=transporter)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        return TransporterDetailsSerializer
