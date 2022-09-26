import abc
from typing import Type

import pandas

from transit.services.pandasToDjango.base import PandasToDjangoMappingAbs


class ExcelUpload:
    def __init__(self, excel_file, mapping_class_type: Type[PandasToDjangoMappingAbs], **kwargs):
        """
        ExcelUpload at first maps xlsx file to pandas DataFrame and then performs operations using pandasToDjango
        services..
        :param excel_file: Data in xlsx format.
        :param kwargs: Passed as kwargs to pandas.read_excel.
        :param mapping_class_type: Class type deriving from PandasToDjangoMappingAbs that provides functionality
        for mapping pandas to django.
        """
        # Ensure proper date format
        self.df = pandas.read_excel(
            excel_file,
            **kwargs
        )
        self.mapping_class = mapping_class_type()
        self.django_models = None

    def map_to_django(self):
        self.django_models = self.mapping_class.map_dataframe_to_django(self.df)
        return self.django_models
