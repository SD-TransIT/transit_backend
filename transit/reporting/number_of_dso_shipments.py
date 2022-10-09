from typing import Dict

import numpy as np
import pandas as pd
from django.core.exceptions import ValidationError
from django.db.models import Sum

from transit.models import ShipmentDetails, DeliveryStatus
from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class NumberOfDSOShipmentsReport(BaseReportGenerator):
    def get_base_queryset(self):
        # Exclude entries without pod variances and precalculate quantities
        return ReportingUtils.get_assigned_shipments() \
            .exclude(pod_variances__isnull=True)\
            .annotate(old_quantities=Sum('order_mapping__order_details__line_items__old_quantity'))\
            .annotate(new_quantities=Sum('order_mapping__order_details__line_items__quantity'))

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'pod_variances__dso_type',
            'old_quantities',
            'new_quantities',
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber', 'DSOType'])
        aggregation = ReportingUtils.shipment_aggregation(
            grouped, ['TransporterName', 'VehicleNumber', 'CustomRouteNumber', 'DSOType']
        )

        pods = pd.DataFrame({
            'OldQuantity': grouped['old_quantities'].agg('sum'),
            'NewQuantity': grouped['new_quantities'].agg('sum'),
        })

        report_data = pd.concat([aggregation, pods], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
