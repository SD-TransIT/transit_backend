import abc
import warnings
from abc import abstractmethod
from typing import Dict

import pandas as pd
from django.db import connections
from django.db.models import QuerySet


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

        :raises: ValueError: if provided filters don't meet criteria.

        :param filters: dictionary with input provided by user.
        :return: Validated filters
        """
        return filters or {}
