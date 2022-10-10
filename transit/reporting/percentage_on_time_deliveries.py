import pandas as pd

from transit.reporting.base_report_generation import BaseReportGenerator
from transit.reporting.reporting_utils import ReportingUtils


class PercentageOnTimeDeliveriesReport(BaseReportGenerator):
    def get_base_queryset(self):
        return ReportingUtils.get_assigned_shipments() \
            .filter(delivery_date__isnull=False)

    def get_queryset_values_list(self, queryset):
        return queryset.values_list(
            *ReportingUtils.get_base_shipment_report_values_list(),
            'delivery_date', 'expected_delivery_date', 'delay_justified'
        )

    def _perform_calculations(self, df, **kwargs):
        df['DeliveryDate'] = df['DeliveryDate'].apply(lambda a: pd.to_datetime(a).date())
        df['ExpectedDeliveryDate'] = df['ExpectedDeliveryDate'].apply(lambda a: pd.to_datetime(a).date())

        grouped = df.groupby(['TransporterID', 'TransporterDetailsID', 'CustomRouteNumber'])
        aggregation = ReportingUtils.vehicle_shipment_aggregation(grouped)
        shipments = pd.DataFrame({
            'Shipments': grouped['id'].agg(pd.Series.nunique),
            'TotalOnTimeDeliveries': grouped['OnTimeDelivery'].agg('sum'),
            'TotalJustifiedDelayedDeliveries': grouped['DelayJustified'].apply(
                lambda x: x is True).count()
        })

        shipments['PercentageOfOnTimeDeliveries'] = \
            ((shipments['TotalOnTimeDeliveries'] / shipments['Shipments']) * 100).round(2)
        shipments['PercentageOfJustifiedDelayedDeliveries'] = \
            ((shipments['TotalJustifiedDelayedDeliveries'] / shipments['Shipments']) * 100).round(2)

        report_data = pd.concat([aggregation, shipments], axis=1)
        report_data.reset_index(drop=True, inplace=True)
        return report_data

    def _preprocess_data_frame(self, df):
        df = ReportingUtils.preprocess_shipment_date(df)
        df['CustomRouteNumber'].replace(to_replace=[None], value='', inplace=True)
        df['OnTimeDelivery'] = df['DeliveryDate'] <= df['ExpectedDeliveryDate']
        df['NotOnTimeDelivery'] = df['DeliveryDate'] > df['ExpectedDeliveryDate']
        return df
