import django_filters
from rest_framework import serializers

from transit.models import ModeOfTransport
from transit.rest_api.abstract import BaseModelFormViewSet


class ModeOfTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeOfTransport
        fields = ['id', 'class_mode', 'vehicle_type']
        read_only_fields = ['id']


class ModeOfTransportFilter(django_filters.FilterSet):
    class Meta:
        model = ModeOfTransport
        fields = {
            'class_mode': ['iexact', 'startswith'],
            'vehicle_type': ['iexact', 'startswith'],
        }
        ordering = ['-id']


class ModeOfTransportViewSet(BaseModelFormViewSet):
    filterset_class = ModeOfTransportFilter
    queryset = ModeOfTransport.objects.all().order_by('-id')
    search_fields = ['id', 'class_mode', 'vehicle_type']

    def get_serializer_class(self):
        return ModeOfTransportSerializer
