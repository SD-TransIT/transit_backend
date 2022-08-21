import django_filters
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from transit.models import Driver
from transit.rest_api.permissions import IsFormsClerk


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['name', 'username', 'password', 'transporter']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
        }


class DriverFilter(django_filters.FilterSet):
    class Meta:
        model = Driver
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'username': ['exact', 'iexact', 'startswith']
        }


class DriverViewSet(viewsets.ModelViewSet):
    filterset_class = DriverFilter
    permission_classes = (IsAuthenticated, IsFormsClerk)
    queryset = Driver.objects.all().order_by('-id')

    def get_serializer_class(self):
        return DriverSerializer
