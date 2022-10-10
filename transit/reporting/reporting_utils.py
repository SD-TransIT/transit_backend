import pandas as pd

from transit.models import ShipmentDetails


class ReportingUtils:  # noqa: PIE798
    @staticmethod
    def vehicle_shipment_aggregation(grouped_df):
        """
        :return: DataFrame in which columns are Shipment Date, Transporter Name, Vehicle Number and Custom Route Number.
        """
        return ReportingUtils.shipment_aggregation(
            grouped_df=grouped_df,
            aggregation_group=['TransporterName', 'VehicleNumber', 'CustomRouteNumber']
        )

    @staticmethod
    def shipment_aggregation(grouped_df, aggregation_group):
        """
        From pandas DataFrameGroupBy object (DataFrame to which groupby() is applied) creates aggregation on
        shipment, transporter name, vehicle number and customer route number.
        :param aggregation_group: List of columns on which group will be mapped.
        :param grouped_df: df.groupby()
        :return: DataFrame in which columns
        """
        grouping_date = grouped_df['ShipDate'].agg(['unique']).rename({'unique': 'ShipmentDate'})
        grouping_date['ShipDate'] = grouping_date['unique'].apply(lambda x: x[0] if len(x) == 1 else 'Many')
        grouping_transporter = grouped_df[aggregation_group].first()
        aggregation = pd.concat([grouping_date, grouping_transporter], axis=1)
        return aggregation.drop(['unique'], axis=1)

    @staticmethod
    def get_assigned_shipments():
        """
        Query returning assigned shipments, defined as shipments with date and transporter assigned. Used
        as entry point for multiple reports.
        :return: queryset on ShipmentDetails
        """
        return ShipmentDetails.objects.filter(
            ship_date__isnull=False,
            transporter_details__transporter__name__isnull=False
        )

    @staticmethod
    def get_invoiced_shipments():
        """
        Query returning invoiced shipments, defined as assigned shipments with cost data.
        :return: queryset on ShipmentDetails
        """
        return ReportingUtils.get_assigned_shipments().filter(transporter_base_cost__isnull=False)

    @staticmethod
    def get_base_shipment_report_values_list():
        """
        Values used commonly in aggregation of data for shipment based reports. Columns included are:
        * Transporter ID and Name
        * Vehicle ID and Number
        * Shipment Date
        * Customer Route Number
        :return: List of ORM references that can be used as input of values_list() on ShipmentDetails.
        """
        return [
            'pk',
            'ship_date',
            'transporter_details__transporter__name', 'transporter_details__transporter__pk',
            'transporter_details__vehicle_number', 'transporter_details__pk',
            'custom_route_number',
        ]

    @staticmethod
    def preprocess_shipment_date(df):
        """
        By default ShipDate is datetime with timzeone info. This function changes type of 'ShipDate'
        column to simple date.
        """
        df['ShipDate'] = df['ShipDate'].apply(lambda a: pd.to_datetime(a).date())
        return df
