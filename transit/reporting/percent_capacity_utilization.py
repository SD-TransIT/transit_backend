from typing import Dict

import numpy as np
import pandas as pd
from django.core.exceptions import ValidationError

from transit.models import ShipmentDetails
from transit.reporting.base_report_generation import BaseReportGenerator


class PercentCapacityUtilizationReport(BaseReportGenerator):
    def get_base_queryset(self):
        return self._get_assigned_shipments()

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            'ship_date', 'transporter_details__transporter__name',
            'transporter_details__vehicle_number',
            'custom_route_number',
            'transporter_details__vehicle_capacity_volume',
            'order_mapping__order_details__line_items__product__volume'
        )

    def _perform_calculations(self, df, **kwargs):
        df = df.copy()
        df['ShipDate'] = df['ShipDate'].apply(lambda a: pd.to_datetime(a).date())
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['volume'].replace(to_replace=[None], value=np.nan, inplace=True)
        grouped = df.groupby(['TransporterName', 'VehicleNumber', 'CustomRouteNumber'])
        grouped_dates = grouped['ShipDate'].agg(['unique'])
        grouped_dates['ShipDate'] = grouped_dates['unique'].apply(lambda x: x[0] if len(x) == 1 else 'Many')
        grouped_dates = grouped_dates.drop(['unique'], axis=1)
        grouped_values = grouped[['VehicleCapacityVolume', 'volume']].sum()
        report_data = pd.concat([grouped_dates, grouped_values], axis=1)
        report_data['PercentUtilization'] = (report_data['volume'] / report_data['VehicleCapacityVolume'] * 100)
        report_data['PercentUtilization'] = report_data['PercentUtilization'].round(2)
        return report_data

    def _get_assigned_shipments(self):
        return ShipmentDetails.objects.filter(
            ship_date__isnull=False,
            transporter_details__transporter__name__isnull=False
        )

    def _validate_filters(self, filters: Dict[str, str]):
        keys = filters.keys()
        if not filters.get('date_from') or not filters.get('date_to') or len(keys) != 2:
            raise ValidationError(
                "Filters for PercentCapacityUtilizationReport should provide only date_from and date_to")
        return {
            'ship_date__gte': filters['date_from'],
            'ship_date__lte': filters['date_to'],
        }
