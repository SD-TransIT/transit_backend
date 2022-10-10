import abc
import datetime
import warnings
from abc import abstractmethod
from typing import Dict

from dateutil import parser
import pandas as pd
from django.core.exceptions import ValidationError
from django.db import connections
from django.db.models import QuerySet
from pytz import timezone

from transit import settings


class BaseReportGenerator(abc.ABC):
    @abstractmethod
    def get_base_queryset(self):
        """
        Queryset, data source that is latter on filtered with user input and transformed to DataFrame.
        :return: QuerySet
        """
        ...

    @abstractmethod
    def get_queryset_values_list(self, queryset):
        """
        Django ORM Queryset .values_list() output. SQL Query product of this operation will be used as pandas
        read_sql() input query. All columns used in aggregations and calculations have to be listed
        as values_list fields.
        :return: QuerySet.values_list()
        """
        ...

    @abstractmethod
    def _perform_calculations(self, df, **kwargs):
        """
        Perform operations on dataframe and returns final form data.

        :param df: DataFrame with data taken from database.
        :param kwargs: Additional parameters used during creation of report. E.g. aggregation level.

        :return: Transformed DataFrame with report data.
        """
        ...

    def __init__(self, filters=None):
        self.filters = self._validate_filters(filters)
        self.base_queryset = self.get_base_queryset()

    def create_report(self, **kwargs):
        user_filtering = self._apply_filters()
        df_input_queryset = self.get_queryset_values_list(user_filtering)
        df = self._read_dataframe_sql(df_input_queryset)
        df = self._preprocess_data_frame(df)
        if df.empty:
            raise ValidationError(F'No data for report for provided filters: \n\t{self.filters}')
        return self._perform_calculations(df, **kwargs)

    def _apply_filters(self):
        return self.base_queryset.filter(**self.filters)

    def _read_dataframe_sql(self, django_queryset: QuerySet):
        db_conn = connections['default']
        query, params = django_queryset.query.sql_with_params()

        # Additional context manager to surpass warning regarding pandas supporting only
        # SQLAlchemy and string URI connection.
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=UserWarning)
            return pd.read_sql(query, db_conn, params=params)

    def _validate_filters(self, filters: Dict[str, str]):
        """
        Additional method allowing validating filters provided during initialization.
        Can be used when report has obligatory filters or if user input has to be alternated.
        Default filters for reports require date_from and date_to filters.

        :raises: ValueError: if provided filters don't meet criteria.

        :param filters: dictionary with input provided by user.
        :return: Validated filters
        """
        keys = filters.keys()
        if not filters.get('date_from') or not filters.get('date_to') or len(keys) != 2:
            raise ValidationError(
                "Filters for PercentCapacityUtilizationReport should provide only date_from and date_to")
        return {
            'ship_date__gte': self.__parse_date(filter_date=filters['date_from']),
            'ship_date__lte': self.__parse_date(filter_date=filters['date_to']),
        }

    def __parse_date(self, filter_date):
        return parser.parse(filter_date).replace(tzinfo=timezone(settings.TIME_ZONE))

    def _preprocess_data_frame(self, df):
        """
        Method is executed before _perform_calculations is called.
        Allows applying additional changes to dataframe before calculations are performed.
        E.g. change data types. By default, no changes are applied.
        :param df:
        :return: preprocessed dataframe
        """
        return df
