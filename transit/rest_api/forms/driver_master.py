import django_filters
from rest_framework import serializers

from transit.models import Driver
from transit.rest_api.abstract import BaseFormViewSet


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['id', 'name', 'username', 'password', 'transporter']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DriverFilter(django_filters.FilterSet):
    class Meta:
        model = Driver
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'username': ['exact', 'iexact', 'startswith']
        }


class DriverViewSet(BaseFormViewSet):
    filterset_class = DriverFilter
    queryset = Driver.objects.all().order_by('-id')

    def get_serializer_class(self):
        return DriverSerializer
