import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from transit.models import Transporter
from transit.rest_api.manual_uploads.fields import FormsDataFields
from transit.rest_api.permissions import IsFormsClerk


class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = [*FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS, 'name', 'phone']
        ordering = ['-id']


class TransporterFilter(django_filters.FilterSet):
    class Meta:
        model = Transporter
        fields = {
            'phone': ['exact', 'iexact'],
            'name': ['exact', 'iexact', 'startswith'],
        }


class TransporterViewSet(viewsets.ModelViewSet):
    filterset_class = TransporterFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = Transporter.objects.all().order_by('-id')

    def get_serializer_class(self):
        return TransporterSerializer
