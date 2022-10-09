import numpy as np
import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerKilometerReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_invoiced_shipments().filter(number_of_kilometers__isnull=False)

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'transporter_base_cost',
            'number_of_kilometers',
            'transporter_additional_cost'
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        combined_cost = grouped[['TransporterBaseCost', 'TransporterAdditionalCost']].sum()
        combined_cost['TotalCost'] = combined_cost['TransporterBaseCost'] + combined_cost['TransporterAdditionalCost']
        combined_km = pd.DataFrame({'TotalNumberOfKilometers': grouped['NumberOfKilometers'].sum()})

        report_data = pd.concat([aggregation, combined_cost, combined_km], axis=1)
        divider = report_data['TotalNumberOfKilometers'].where(report_data['TotalNumberOfKilometers'] != 0, np.nan)
        report_data['AverageCostPerKilometer'] = report_data['TotalCost'].divide(divider).astype(float).round(2)

        report_data.reset_index(drop=True, inplace=True)
        return report_data[[
            'ShipDate', 'TransporterName', 'VehicleNumber', 'CustomRouteNumber',
            'TotalCost', 'TotalNumberOfKilometers', 'AverageCostPerKilometer'
        ]]

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['TransporterAdditionalCost'].replace(to_replace=[None], value=0.0, inplace=True)
        return df
