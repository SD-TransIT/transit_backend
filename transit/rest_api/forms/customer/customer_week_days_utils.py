from rest_framework import serializers

from transit.models import CustomerWeekDays, Customer
from transit.rest_api.forms.customer.week_days import CustomerWeekDaysSerializer
from transit.services.customer_working_hours_service import CustomerWeekdaysService


class CustomerWeekDaysSerializerOptionalCustomer(CustomerWeekDaysSerializer):
    """
    Extension of CustomerWeekDaysSerializer that allows creating working hours directly from
    customer endpoint.
    """
    customer = serializers.ModelField(Customer()._meta.pk, required=False)


class CustomerWeekDaysSerializerWrapper(serializers.Serializer):
    """
    Utilizes CustomerWeekDaysSerializer for purpose of bulk replacement of working hours.
    """
    _service = CustomerWeekdaysService()

    week_days = serializers.ListField(
        child=CustomerWeekDaysSerializerOptionalCustomer(), required=True, allow_empty=True
    )

    def update(self, instance, validated_data):
        raise NotImplementedError('update() not supported in WorkhoursSerializer,'
                                  ' data should be alternated using replace_working_hours')

    def create(self, validated_data):
        raise NotImplementedError('create() not supported in WorkhoursSerializer,'
                                  ' data should be alternated using replace_working_hours')

    def replace_working_hours(self):
        week_days = [CustomerWeekDays(**day) for day in self.validated_data['week_days']]
        self._service.replace_customer_weekdays(customer=self.instance, weekdays=week_days)

    def to_internal_value(self, data):  # noqa: WPS122
        # As customer is ModelField it will not be automatically bind to customer object
        internal = super(CustomerWeekDaysSerializerWrapper, self).to_internal_value(data)
        for week_day in internal['week_days']:
            week_day['customer'] = Customer.objects.get(pk=internal['customer']) if 'customer' in internal else None
        return internal

    def to_representation(self, instance):
        field = self.fields['week_days']
        return field.to_representation(instance.week_days.all())
