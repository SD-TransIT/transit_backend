import django_filters
from rest_framework import serializers

from transit.models import Transporter
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.forms.fields import FormsDataFields


class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = ['id', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS, 'name', 'phone']
        read_only_fields = ['id']
        ordering = ['-id']


class TransporterFilter(django_filters.FilterSet):
    class Meta:
        model = Transporter
        fields = {
            'phone': ['exact', 'iexact'],
            'name': ['exact', 'iexact', 'startswith'],
        }


class TransporterViewSet(BaseFormViewSet):
    filterset_class = TransporterFilter
    queryset = Transporter.objects.all().order_by('-id')

    def get_serializer_class(self):
        return TransporterSerializer
