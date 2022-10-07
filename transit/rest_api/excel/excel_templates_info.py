import pandas as pd

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from transit.rest_api.excel.example_excel_data import (
    CUSTOMER_EXAMPLE_DATA,
    ITEM_DETAILS_EXAMPLE_DATA,
    ITEM_MASTER_EXAMPLE_DATA,
    ORDER_DETAILS_EXAMPLE_DATA,
    SUPPLIER_EXAMPLE_DATA
)


class ExcelTemplatesInfo(serializers.Serializer):
    excel_example_data = {
        'customer_master': CUSTOMER_EXAMPLE_DATA,
        'item_details': ITEM_DETAILS_EXAMPLE_DATA,
        'item_master': ITEM_MASTER_EXAMPLE_DATA,
        'order_details': ORDER_DETAILS_EXAMPLE_DATA,
        'supplier_master': SUPPLIER_EXAMPLE_DATA,
    }

    def get_example_data_for_excel(self, form_type):
        return self.excel_example_data[form_type]


excel_upload_type_param = openapi.Parameter(
    'form_type',
    openapi.IN_QUERY,
    description="type of excel upload form",
    type=openapi.TYPE_STRING
)


class ExcelTemplatesInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for download excel file template.
    """
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[excel_upload_type_param])
    def list(self, request):
        form_type = self.request.GET.get('form_type', None)
        if form_type and form_type in ExcelTemplatesInfo().excel_example_data:
            filename = f"template_{form_type}"
            df = pd.DataFrame(ExcelTemplatesInfo().get_example_data_for_excel(form_type))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
            df.to_excel(response, index=False)
            return response
        else:
            raise ValidationError(_('Bad request. Such kind of excel upload does not exist in system.'))
