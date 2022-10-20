import django_filters
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from transit.models import CustomerWeekDays
from transit.rest_api.abstract import BaseModelFormViewSet


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


class CustomerWeekDaysViewSet(BaseModelFormViewSet):
    filterset_class = CustomerWeekDaysFilter
    queryset = CustomerWeekDays.objects.all().order_by('-id')
    pagination_class = None

    def get_serializer_class(self):
        return CustomerWeekDaysSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request, *args, **kwargs):
        week_days_creation_result = self._create_inputs(request.data)
        return Response(week_days_creation_result, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def _create_inputs(self, list_of_week_days):
        outputs = []
        for week_day_element in list_of_week_days:
            serializer = self.get_serializer(data=week_day_element)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            outputs.append(serializer.data)
        return outputs
