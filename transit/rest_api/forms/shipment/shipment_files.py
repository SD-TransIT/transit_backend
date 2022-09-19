from rest_framework import serializers, filters
from rest_framework.parsers import MultiPartParser

from transit.models.shipment import ShipmentDetailFiles
from transit.rest_api.abstract import BaseModelFormViewSet


class ShipmentDetailFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetailFiles
        fields = ('id', 'shipment', 'file')
        read_only_fields = ['id']
        ordering = ['-id']


class ShipmentDetailFilesViewSet(BaseModelFormViewSet):
    parser_classes = (MultiPartParser,)
    queryset = ShipmentDetailFiles.objects.all()
    serializer_class = ShipmentDetailFilesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['shipment__id']

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')
