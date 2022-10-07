from django.http import (
    Http404,
    HttpResponse
)
from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class ExcelTemplatesInfo(serializers.Serializer):
    excel_example_data = {
        'customer_master': 'transit/rest_api/excel/excel_template_files/CustomerMasterExample.xlsx',
        'item_details': 'transit/rest_api/excel/excel_template_files/ItemDetailsExample.xlsx',
        'item_master': 'transit/rest_api/excel/excel_template_files/ItemMasterExample.xlsx',
        'order_details': 'transit/rest_api/excel/excel_template_files/OrderDetailsExample.xlsx',
        'supplier_master': 'transit/rest_api/excel/excel_template_files/SupplierMasterExample.xlsx',
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
            file_path = ExcelTemplatesInfo().get_example_data_for_excel(form_type)
            file_name = file_path.split('/').pop()
            try:
                with open(file_path, 'rb') as document:
                    response = HttpResponse(
                        document,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = f'attachment; filename={file_name}'
                    return response
            except IOError:
                raise Http404(_('There is a problem with processing such file.'))
        else:
            raise ValidationError(_('Bad request. Such kind of excel upload does not exist in system.'))
