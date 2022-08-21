import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import ModeOfTransport
from transit.rest_api.permissions import IsFormsClerk


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


class ModeOfTransportViewSet(viewsets.ModelViewSet):
    filterset_class = ModeOfTransportFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = ModeOfTransport.objects.all().order_by('-id')

    def get_serializer_class(self):
        return ModeOfTransportSerializer
