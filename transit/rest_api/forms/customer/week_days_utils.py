from rest_framework import serializers

from transit.models import CustomerWeekDays
from transit.rest_api.forms.customer.customer_week_days import CustomerWeekDaysSerializer
from transit.services.customer_working_hours_service import CustomerWeekdaysService


class CustomerWeekDaysSerializerWrapper(serializers.Serializer):
    # Instance of serializer that allows replacing week days directly from customer
    _service = CustomerWeekdaysService()

    week_days = serializers.ListField(
        child=CustomerWeekDaysSerializer(), required=True, allow_empty=False
    )  # Ids of orders relevant for given shipment, handled by ShipmentDetails manager.

    def update(self, instance, validated_data):
        raise NotImplementedError('update() not supported in WorkhoursSerializer,'
                                  ' data should be alternated using replace_working_hours')

    def create(self, validated_data):
        raise NotImplementedError('create() not supported in WorkhoursSerializer,'
                                  ' data should be alternated using replace_working_hours')

    def replace_working_hours(self):
        week_days = [CustomerWeekDays(**day) for day in self.validated_data['week_days']]
        self._service \
            .replace_customer_weekdays(customer=self.instance, weekdays=week_days)

    def to_representation(self, instance):
        field = self.fields['week_days']
        return field.to_representation(instance.week_days.all())
