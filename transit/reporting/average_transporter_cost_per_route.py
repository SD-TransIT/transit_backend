import pandas as pd
from django.db.models import Q

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerRouteReport(BaseReportGenerator):
    def get_base_queryset(self):
        # Report only for shipments where custom route available
        return ReportingUtils.get_assigned_shipments().filter(
            ~(Q(custom_route_number__isnull=True) | Q(custom_route_number=''))
        )

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'transporter_base_cost',
            'transporter_additional_cost'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID'])
        aggregation = ReportingUtils.shipment_aggregation(grouped, ['TransporterName', 'VehicleNumber'])

        combined_cost = grouped[['TransporterBaseCost', 'TransporterAdditionalCost']].sum()
        combined_cost['TotalCost'] = combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost']

        totals = pd.DataFrame({
            'CustomRoutes': grouped['CustomRouteNumber'].agg(pd.Series.nunique),
            'TotalCost': combined_cost['TotalCost']
        })
        totals['AverageTransporterCostPerRoute'] = totals['TotalCost'] / totals['CustomRoutes']
        report_data = pd.concat([aggregation, totals], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
