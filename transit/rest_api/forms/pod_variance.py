import django_filters
from rest_framework import serializers

from transit.models import PODVariance
from transit.rest_api.abstract import BaseFormViewSet


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


class PODVarianceViewSet(BaseFormViewSet):
    filterset_class = PODVarianceFilter
    queryset = PODVariance.objects.all().order_by('-id')

    def get_serializer_class(self):
        return PODVarianceSerializer
