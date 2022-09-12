import django_filters
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from transit.models import Customer, CustomerWeekDays
from transit.rest_api.abstract import BaseFormViewSet
from transit.rest_api.forms.fields import FormsDataFields


class CustomerWeekDaysSerializerWrapper(serializers.ModelSerializer):
    # Instance of serializer that allows creating week days directly from customer
    class Meta:
        model = CustomerWeekDays
        fields = [
            'id', 'day', 'opening_time', 'closing_time', 'closed',
            'meridiem_indicator_opening_time', 'meridiem_indicator_closing_time'
        ]
        read_only_fields = ['id']
        ordering = ['-id']


class CustomerSerializer(serializers.ModelSerializer):
    customer_type_name = serializers.CharField(source='customer_type.customer_type_name', read_only=True)
    week_days = CustomerWeekDaysSerializerWrapper(many=True, required=False)

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
        if self.instance and validated.get('line_items'):
            raise serializers.ValidationError(
                _("Customer week days have to be updated using customer_week_days endpoint.")
            )
        return validated


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'iexact', 'startswith'],
            'first_name': ['exact', 'iexact', 'startswith'],
            'last_name': ['exact', 'iexact', 'startswith'],
        }


class CustomerViewSet(BaseFormViewSet):
    filterset_class = CustomerFilter
    queryset = Customer.objects.all().order_by('-id')
    search_fields = [
        'id', *FormsDataFields.GEOGRAPHICAL_MODEL_FIELDS,
        'name', 'first_name', 'last_name', 'phone', 'email', 'customer_type__customer_type_name'
    ]

    def get_serializer_class(self):
        return CustomerSerializer
