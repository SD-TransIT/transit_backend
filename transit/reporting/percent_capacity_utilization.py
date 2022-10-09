import numpy as np
import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class PercentCapacityUtilizationReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_assigned_shipments()

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'transporter_details__vehicle_capacity_volume',
            'order_mapping__order_details__line_items__product__volume'
        )

    def _perform_calculations(self, df, **kwargs):
        df = df.copy()
        df['ShipDate'] = df['ShipDate'].apply(lambda a: pd.to_datetime(a).date())
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['volume'].replace(to_replace=[None], value=np.nan, inplace=True)
        grouped = df.groupby(['TransporterName', 'VehicleNumber', 'CustomRouteNumber'])

        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)
        grouped_values = grouped[['VehicleCapacityVolume', 'volume']].sum()

        report_data = pd.concat([aggregation, grouped_values], axis=1)
        report_data['PercentUtilization'] = (report_data['volume'] / report_data['VehicleCapacityVolume'] * 100)
        report_data['PercentUtilization'] = report_data['PercentUtilization'].round(2)

        # Index is dropped as aggregation is already included in DF
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['VehicleNumber'].replace(to_replace=[None], value='', inplace=True)
        df['volume'].replace(to_replace=[None], value=np.nan, inplace=True)
        return df
