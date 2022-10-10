import numpy as np
import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class AverageKilometersPerShipmentByTransporterReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_invoiced_shipments().filter(number_of_kilometers__isnull=False)

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'number_of_kilometers',
        )

    def _perform_calculations(self, df, **kwargs):
        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)

        total_shipments = pd.DataFrame({'TotalNumberOfShipments': grouped['id'].agg(pd.Series.nunique)})
        total_km = pd.DataFrame({'TotalKilometers': grouped['NumberOfKilometers'].sum()})

        report_data = pd.concat([aggregation, total_shipments, total_km], axis=1)
        divider = report_data['TotalNumberOfShipments'].where(report_data['TotalNumberOfShipments'] != 0, np.nan)
        report_data['AverageKilometersPerShipment'] = report_data['TotalKilometers']\
            .divide(divider).astype(float).round(2)

        report_data.reset_index(drop=True, inplace=True)
        return report_data[[
            'ShipDate', 'TransporterName', 'VehicleNumber', 'CustomRouteNumber',
            'TotalNumberOfShipments', 'TotalKilometers', 'AverageKilometersPerShipment'
        ]]

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        return df
