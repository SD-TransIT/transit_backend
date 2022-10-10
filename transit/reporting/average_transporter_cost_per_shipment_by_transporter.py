import numpy as np
import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerShipmentByTransporterReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_invoiced_shipments()

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'transporter_base_cost',
            'transporter_additional_cost'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        total_shipments = pd.DataFrame({'TotalNumberOfShipments': grouped['id'].agg(pd.Series.nunique)})
        combined_cost = grouped[['TransporterBaseCost', 'TransporterAdditionalCost']].sum()
        combined_cost['TotalTransporterCost'] = \
            combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost']

        report_data = pd.concat([aggregation, total_shipments, combined_cost], axis=1)
        divider = report_data['TotalNumberOfShipments'].where(report_data['TotalNumberOfShipments'] != 0, np.nan)
        report_data['AverageTransporterCostPerShipment'] = report_data['TotalTransporterCost']\
            .divide(divider).astype(float).round(2)

        report_data.reset_index(drop=True, inplace=True)
        return report_data[[
            'ShipDate', 'TransporterName', 'VehicleNumber', 'CustomRouteNumber',
            'TotalTransporterCost', 'TotalNumberOfShipments', 'AverageTransporterCostPerShipment'
        ]]

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['TransporterAdditionalCost'].replace(to_replace=[None], value=0.0, inplace=True)
        return df
