import abc
import logging
from typing import Type

import pandas
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from transit.services.excelUpload import ExcelUpload
from transit.services.pandasToDjango.base import PandasToDjangoMappingAbs
from transit.services.pandasToDjango.mappings import ItemMasterMapping, CustomerDetailMapping, ItemDetailMapping, \
    OrderDetailsMapping, SupplierMasterMapping

logger = logging.getLogger(__name__)


class BaseExcelUploadViewSet(abc.ABC, GenericViewSet):
    parser_classes = (MultiPartParser,)

    # Columns of text type that should be parsed as dates.
    parse_dates = []

    # Used to ensure that correct data types are used (e.g. phone number could be treated as number not str).
    converters = {}

    @staticmethod
    def date_parser(date):
        try:
            return pandas.datetime.strptime(date, "%d/%m/%Y")
        except TypeError as e:
            logger.warning("Invalid datetime format in excel upload, "
                           "expected Text column with data in format %s, detail: %s", '%d/%m/%Y', e)
            return date

    @property
    @abc.abstractmethod
    def mapping_class(self) -> Type[PandasToDjangoMappingAbs]:
        """
        Mapping class allowing mapping from Pandas dataframe (to which Excel field is cast) to django objects.
        :return: instance of class deriving from PandasToDjangoMappingAbs
        """
        ...

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(
            'file', openapi.IN_FORM, type=openapi.TYPE_FILE,
            description='Excel file.', required=True
        )],
        operation_description="Allows uploading file in Excel format",
        responses={204: 'Data from file successfully uploaded'})
    def create(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            raise ValueError(_("File not provided"))
        # Temporarily save file on server. As it's not meant to be stored permanently, media root is not used.
        excel_handler = ExcelUpload(
            file_obj, self.mapping_class,
            parse_dates=self.parse_dates,
            date_parser=self.date_parser,
            converters=self.converters
        )
        django_objects = excel_handler.map_to_django()
        self.save_objects(django_objects)
        return Response(status=204)

    @transaction.atomic
    def save_objects(self, django_objects):
        self.mapping_class.model.objects.bulk_create(django_objects)


class ItemMasterExcelUploadView(BaseExcelUploadViewSet):
    mapping_class = ItemMasterMapping


class ItemDetailExcelUploadView(BaseExcelUploadViewSet):
    mapping_class = ItemDetailMapping
    parse_dates = ['Expiry Date', 'Date of Manufacture', 'Date Received']
    converters = {'GTIN': int, 'Lot Number': str, 'Serial Number': str}


class CustomerDetailExcelUploadView(BaseExcelUploadViewSet):
    converters = {'Phone': str}
    mapping_class = CustomerDetailMapping


class SupplierExcelUploadView(BaseExcelUploadViewSet):
    converters = {'Phone': str}
    mapping_class = SupplierMasterMapping


class OrderDetailsExcelUploadView(BaseExcelUploadViewSet):
    mapping_class = OrderDetailsMapping

    @transaction.atomic
    def save_objects(self, django_objects):
        lit = {}
        # At first line items are moved from objects - due to usage of related manager they couldn't be stored in
        # obj.line_items, therefore they were passed as extra line_items_temp argument.
        for order_detail in django_objects:
            lit[order_detail] = order_detail.line_items_temp
            del order_detail.line_items_temp  # noqa: WPS100

        # Orders are saved
        self.mapping_class.model.objects.bulk_create(django_objects)

        # Stored order line is assigned to order line details before they're saved
        for order_detail, line_items in lit.items():
            for line_item in line_items:
                # Line item is also created in mapping process, not taken from database
                line_item.item_details.save()
                line_item.order_details = order_detail
            self.mapping_class.line_details_mapping.model.objects.bulk_create(line_items)
