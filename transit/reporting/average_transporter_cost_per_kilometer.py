from typing import Dict

import numpy as np
import pandas as pd
from django.core.exceptions import ValidationError

from transit.models import ShipmentDetails
from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageTransporterCostPerKilometerReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_assigned_shipments()

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
        report_data['AverageCostPerKilometer'] = \
            (report_data['TotalCost'] / report_data['TotalNumberOfKilometers']).round(2)

        report_data.reset_index(drop=True, inplace=True)
        report_data = report_data[[
            'ShipDate', 'TransporterName', 'VehicleNumber', 'CustomRouteNumber',
            'TotalCost', 'TotalNumberOfKilometers', 'AverageCostPerKilometer'
        ]]

        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
