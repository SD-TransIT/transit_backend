import django_filters
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from transit.models import Customer, CustomerWeekDays
from transit.rest_api.abstract import BaseModelFormViewSet
from transit.rest_api.forms.customer.week_days import CustomerWeekDaysSerializer
from transit.rest_api.forms.customer.customer_week_days_utils import CustomerWeekDaysSerializerWrapper, \
    CustomerWeekDaysSerializerOptionalCustomer
from transit.rest_api.forms.fields import FormsDataFields


class CustomerSerializer(serializers.ModelSerializer):
    customer_type_name = serializers.CharField(source='customer_type.customer_type_name', read_only=True)
    week_days = CustomerWeekDaysSerializerOptionalCustomer(many=True, required=False)

    class Meta:
        model = Customer
        fields = [
            'id', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS,
            'name', 'first_name', 'last_name', 'phone', 'email', 'customer_type', 'customer_type_name',
            'week_days'
        ]
        read_only_fields = ['id']
        ordering = ['-id']

    def create(self, validated_data):
        return self._create_customer(validated_data)

    @transaction.atomic
    def _create_customer(self, validated_data):
        week_days = validated_data.pop('week_days', [])
        customer = Customer.objects.create(**validated_data)
        for item_dict in week_days:
            item_dict['customer'] = customer
            CustomerWeekDays(**item_dict).save()
        return customer  # noqa: R504

    def validate(self, data): # noqa: WPS-122
        """
        Update of working hours directly through Customer is forbidden.
        """
        validated = super(CustomerSerializer, self).validate(data)
        self._validate_update_payload(validated)
        return validated

    def _validate_update_payload(self, validated):
        if self.instance and validated.get('line_items'):
            raise serializers.ValidationError(
                _("Customer week days have to be updated using /api/customer_week_days "
                  "or /api/customer/{id}/replace_working_hours endpoints.")
            )


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'first_name': ['exact', 'iexact', 'startswith'],
            'last_name': ['exact', 'iexact', 'startswith'],
        }


class CustomerViewSet(BaseModelFormViewSet):
    queryset = Customer.objects.all().order_by('-id')

    filterset_class = CustomerFilter
    search_fields = [
        'id', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS,
        'name', 'first_name', 'last_name', 'phone', 'email', 'customer_type__customer_type_name'
    ]

    _workhours_serializer = CustomerWeekDaysSerializerWrapper

    def get_serializer_class(self):
        return CustomerSerializer

    @swagger_auto_schema(methods=['post'], request_body=CustomerWeekDaysSerializer)
    @action(detail=True, methods=['post'])
    def replace_working_hours(self, request, pk=None):
        serializer = self._build_workhours_serializer(request)
        serializer.replace_working_hours()
        return self._valid_work_hours(serializer)

    def _build_workhours_serializer(self, request):
        customer = self.get_object()
        serializer = self._workhours_serializer(instance=customer, data=request.data)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        return serializer

    def _valid_work_hours(self, serializer):
        return Response(serializer.to_representation(self.get_object()), status=status.HTTP_200_OK)
