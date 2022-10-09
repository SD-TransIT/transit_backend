import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageProductCostPerShipmentReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_assigned_shipments()

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'order_mapping__order_details__line_items__product__cost'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        combined_cost = grouped[['Cost']].sum()
        shipments = pd.DataFrame({'Shipments': grouped['id'].agg(pd.Series.nunique)})

        report_data = pd.concat([aggregation, combined_cost, shipments], axis=1)
        report_data['AverageCost'] = (report_data['Cost'] / shipments['Shipments']).round(2)

        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
