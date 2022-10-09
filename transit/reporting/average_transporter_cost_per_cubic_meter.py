import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerCubicMeterReport(BaseReportGenerator):
    def get_base_queryset(self):
        # Exclude shipments where volumetric data is not fully available
        return ReportingUtils.get_assigned_shipments().exclude(
            order_mapping__order_details__line_items__product__volume__isnull=True
        )

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'order_mapping__order_details__line_items__product__volume',
            'transporter_base_cost',
            'transporter_additional_cost'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        combined_cost = grouped[['TransporterBaseCost', 'TransporterAdditionalCost']].sum()
        combined_cost['TotalCost'] = combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost']

        totals = pd.DataFrame({
            'TotalVolume': grouped['volume'].sum(),
            'TotalCost': combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost'],
        })

        totals['AverageTransporterCostPerCubicMeter'] = totals['TotalCost']/totals['TotalVolume']
        report_data = pd.concat([aggregation, totals], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
