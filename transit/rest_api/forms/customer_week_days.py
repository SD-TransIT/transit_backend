import django_filters
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from transit.models import Customer, CustomerWeekDays
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.forms.fields import FormsDataFields


class CustomerWeekDaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerWeekDays
        fields = [
            'id', 'day', 'customer', 'opening_time', 'closing_time', 'closed',
            'meridiem_indicator_opening_time', 'meridiem_indicator_closing_time'
        ]
        read_only_fields = ['id']
        ordering = ['-id']


class CustomerWeekDaysFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerWeekDays
        fields = {
            'customer': ['exact'],
            'opening_time': ['exact', 'iexact'],
            'closing_time': ['exact', 'iexact'],
            'meridiem_indicator_opening_time': ['exact', 'iexact'],
            'meridiem_indicator_closing_time': ['exact', 'iexact'],
            'closed': ['exact'],
        }


class CustomerWeekDaysViewSet(BaseFormViewSet):
    filterset_class = CustomerWeekDaysFilter
    queryset = CustomerWeekDays.objects.all().order_by('-id')

    def get_serializer_class(self):
        return CustomerWeekDaysSerializer
