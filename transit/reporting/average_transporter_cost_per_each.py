import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerEachReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_invoiced_shipments()

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'transporter_base_cost',
            'transporter_additional_cost',
            'order_mapping__order_details__line_items__quantity'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        combined_cost = grouped[['TransporterBaseCost', 'TransporterAdditionalCost']].sum()
        combined_cost['TotalCost'] = combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost']

        totals = pd.DataFrame({
            'TotalEaches': grouped['Quantity'].sum(),
            'TotalCost': combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost'],
        })

        totals['AverageTransporterCostPerEach'] = totals['TotalCost'] / totals['TotalEaches']
        report_data = pd.concat([aggregation, totals], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['TransporterBaseCost'].replace(to_replace=[None], value=0.0, inplace=True)
        df['TransporterAdditionalCost'].replace(to_replace=[None], value=0.0, inplace=True)
        return df
