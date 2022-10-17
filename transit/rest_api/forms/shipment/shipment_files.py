import django_filters

from rest_framework import serializers
from rest_framework.parsers import MultiPartParser

from transit.models.shipment import ShipmentDetailFiles
from transit.rest_api.abstract import BaseModelFormViewSet


class ShipmentDetailFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetailFiles
        fields = ('id', 'shipment', 'file')
        read_only_fields = ['id']
        ordering = ['-id']


class ShipmentDetailFilesFilter(django_filters.FilterSet):
    class Meta:
        model = ShipmentDetailFiles
        fields = {
            'id': ['exact', 'iexact', 'startswith'],
            'shipment__id': ['exact']
        }


class ShipmentDetailFilesViewSet(BaseModelFormViewSet):
    parser_classes = (MultiPartParser,)
    queryset = ShipmentDetailFiles.objects.all()
    serializer_class = ShipmentDetailFilesSerializer
    filterset_class = ShipmentDetailFilesFilter
    pagination_class = None
    search_fields = ['shipment__id']

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')
