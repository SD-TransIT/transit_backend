from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class OrdersReadyToBeShippedReport(BaseReportGenerator):
    def get_base_queryset(self):
        # Produces a list of orders generated which are ready to be shipped but which have not yet been completed.
        return ReportingUtils.get_assigned_shipments().filter(delivery_date__isnull=True)

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            'pk',
            'order_mapping__order_details__order_details_id',
            'order_mapping__order_details__customer__name',
            'order_mapping__order_details__customer__address_1',
            'order_mapping__order_details__customer__address_2',
            'order_mapping__order_details__customer__address_3',
            'order_mapping__order_details__customer__city',
            'order_mapping__order_details__customer__country',
            'order_mapping__order_details__customer__state',
        )

    def _perform_calculations(self, df, **kwargs):
        return df.rename(columns={
            'id': 'ShipmentNumber',
            'OrderDetailsID': 'OrderNumber'
        })
