from typing import Collection

from django.db import transaction

from transit.models import OrderDetails, CustomerWeekDays, Customer


class CustomerWeekdaysService:

    @transaction.atomic
    def replace_customer_weekdays(self, customer: Customer, weekdays: Collection[CustomerWeekDays]):
        """
        Overwrite CustomerWeekDays for given customer with `weekdays`. If any prior `weekdays` were assigned to
        customer and are not part of weekdays - they will be removed.

        :param customer: customer to which weekdays will be assigned.
        :param weekdays: List of CustomerWeekDays elements.
        :return: Collection of CustomerWeekDays
        """
        # Remove weekdays that are existing for customer but not part of payload
        self._remove_all_customer_days(customer)
        # Add new customer weekdays
        self._create_new_weekdays(customer, weekdays)
        return customer.week_days

    def _remove_all_customer_days(self, customer: Customer):
        not_included = CustomerWeekDays.objects.filter(customer=customer)
        not_included.all().delete()

    def _create_new_weekdays(self, customer: Customer, weekdays: Collection[CustomerWeekDays]):
        for day in weekdays:
            day.customer = customer
        CustomerWeekDays.objects.bulk_create(weekdays)

    def _existing_weekdays(self, weekdays):
        return CustomerWeekDays.objects.filter(pk__in=[day.pk for day in weekdays])

    def _get_weekdays_without_customer(self, weekdays):
        return OrderDetails.objects.filter(pk__in=[order.pk for order in weekdays]).without_customer_details().all()
