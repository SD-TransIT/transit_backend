import django_filters
from rest_framework import serializers

from transit.models import ModeOfTransport
from transit.rest_api.abstract import BaseFormViewSet


class ModeOfTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeOfTransport
        fields = ['class_mode', 'vehicle_type']


class ModeOfTransportFilter(django_filters.FilterSet):
    class Meta:
        model = ModeOfTransport
        fields = {
            'class_mode': ['iexact', 'startswith'],
            'vehicle_type': ['iexact', 'startswith'],
        }
        ordering = ['-id']


class ModeOfTransportViewSet(BaseFormViewSet):
    filterset_class = ModeOfTransportFilter
    queryset = ModeOfTransport.objects.all().order_by('-id')

    def get_serializer_class(self):
        return ModeOfTransportSerializer