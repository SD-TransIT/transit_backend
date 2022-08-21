import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import PODVariance
from transit.rest_api.permissions import IsFormsClerk


class PODVarianceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PODVariance
        fields = ['dso_type', 'shipment']
        ordering = ['-id']


class PODVarianceFilter(django_filters.FilterSet):
    class Meta:
        model = PODVariance
        fields = {
            'dso_type': ['exact', 'iexact', 'startswith']
        }


class PODVarianceViewSet(viewsets.ModelViewSet):
    filterset_class = PODVarianceFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = PODVariance.objects.all().order_by('-id')

    def get_serializer_class(self):
        return PODVarianceSerializer
