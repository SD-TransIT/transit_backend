import pandas as pd
from django.db.models import Sum

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class OrdersWithNoShippingDetailsReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_shipments_with_missing_details()

    def get_queryset_values_list(self, queryset):
        return queryset\
            .annotate(volume=Sum('order_mapping__order_details__line_items__product__volume'))\
            .annotate(quantity=Sum('order_mapping__order_details__line_items__quantity'))\
            .values_list(*ReportingUtils.get_base_shipment_report_values_list(), 'volume', 'quantity')

    def _perform_calculations(self, df, **kwargs):
        report_data = pd.DataFrame({
            'ShipmentNumber': df['id'],
            'ShipmentVolume': df['volume'] * df['quantity']
        })
        return report_data.reset_index(drop=True)
