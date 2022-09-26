import abc
from typing import Dict, Callable, Any, Type, List

import pandas
from django.db import models
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _
from numpy import nan
from pandas import DataFrame
from pydantic.dataclasses import dataclass


class PandasMappingError(Exception):
    def __init__(self, **kwargs):
        self.message = kwargs['message']
        super().__init__(self.message)


@dataclass
class PandasCellMappingDefinition:
    """
    Class used for defining how given cell values should be mapped and to which django field
    they are assigned. By default, value in returned in format proper for given column.
    """
    django_model_field: str
    mapping_function: Callable[[Any], Any] = lambda x: x


class PandasToDjangoMappingAbs(abc.ABC):
    @classproperty
    @abc.abstractmethod
    def model(self) -> Type[models.Model]:
        """
        Type of django model to which Pandas rows will be mapped.
        :return: models.Model
        """
        ...

    @property
    @abc.abstractmethod
    def mapping_definition(self) -> Dict[str, PandasCellMappingDefinition]:
        """
        Dict with mapping definition where key is pandas column name and value is a function mapping cell value from
        given column to value accepted django model field name.

        :Example:

        >>>{
        ...   'Customer ID': PandasCellMappingDefinition('customer_type_name',
        ...       lambda x: return CustomerType.objects.get(name=x)
        ...   )
        ...}

        :return: models.Model
        """
        ...

    @property
    def excluded_fields(self) -> List[str]:
        """
        If provided dataframe contains rows that should not be considered during mapping,
        these fields should be explicitly provided under excluded fields.

        :Example:

        >>>excluded_fields = ['Item Code', 'Item Value']

        will exclude columns 'Item Code', 'Item Value' from calculations.

        :return: List of DataFrame column names.
        """
        return []

    def map_dataframe_to_django(self, pandas_rows: DataFrame) -> List[models.Model]:
        """
        Calls map_pandas_row for all rows in DataFrame.
        :param pandas_rows: DataFrame with model data
        :return: List of Django objects.
        """
        df = pandas_rows.loc[:, ~pandas_rows.columns.isin(self.excluded_fields)]
        # Replace nan with None - this changes dtype of all columns to objects
        df = df.replace({nan: None})
        errors = {}
        django_objects = []

        for index, row in df.iterrows():
            try:
                django_objects.append(self._map_pandas_row(row))
            except PandasMappingError as e:
                errors[index] = e.message
        if errors:
            raise PandasMappingError(message=str(errors))
        return django_objects

    def _map_pandas_row(self, row_data: pandas.Series) -> models.Model:
        """
        Dict representing pandas data row. Key is column header and value is cell value in string format.
        All data mappings to other formats shoul be done within  PandasCellMappingDefinition.mapping_function
        :param row_data: Dict representing data.
        :return: Django Model with values from taken from row. It is not saved in database.
        """
        django_data, errors = self._map_row(row_data)
        if errors:
            raise PandasMappingError(message=str(errors))
        return self.model(**django_data)

    def _map_row(self, row_data: pandas.Series):
        errors = {}
        django_data = {}
        for model_attribute, model_value in row_data.items():
            try:
                mapping: PandasCellMappingDefinition = self.mapping_definition[str(model_attribute)]
                django_data[mapping.django_model_field] = mapping.mapping_function(model_value)
            except Exception as exc:  # noqa: PIE786
                errors[model_attribute] =\
                    _("Error occurred during mapping value %s, details: %s") % (model_value, str(exc))
        return django_data, errors
