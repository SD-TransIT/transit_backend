from typing import Dict

import numpy as np
import pandas as pd
from django.core.exceptions import ValidationError

from transit.models import ShipmentDetails, DeliveryStatus
from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class PercentageOutstandingPODsReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_assigned_shipments() \
            .filter(delivery_status__delivery_status=DeliveryStatus.Status.DELIVERED)

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'pod_status__delivery_status'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        pods = pd.DataFrame({
            'TotalPODs': grouped['id'].agg(pd.Series.nunique),
            # Delivered shipments but without delivered POD
            'OutstandingPODs': grouped['DeliveryStatus'].agg('unique').apply(
                lambda x: (x != DeliveryStatus.Status.DELIVERED)).count()
        })

        pods['PercentageOfOutstandingPODs'] = ((pods['OutstandingPODs'] / pods['TotalPODs']) * 100).round(2)

        report_data = pd.concat([aggregation, pods], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['VehicleNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
