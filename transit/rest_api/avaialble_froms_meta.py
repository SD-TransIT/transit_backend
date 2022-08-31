import logging

from django.http import Http404
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transit.rest_api.forms_router import manual_forms


class FormsInfo(serializers.Serializer):
    form_names = {
        'supplier': _('Supplier Master'),
        'customer_type': _('Customer Type'),
        'customer': _('Customer Master'),
        'mode_of_transport': _('Mode of Transport Master'),
        'item': _('Item Master'),
        'item_details': _('Item Details'),
        'transporter_details': _('Transporter Details'),
        'driver': _('Driver Master'),
        'order_details': _('Order Details'),
        'shipment_details': _('Shipment'),
        'cost': _('Cost Form'),
        'pod_variance': _('POD Variance'),
    }

    def get_available_forms(self):
        routed_forms = manual_forms()
        available_forms = []
        for form in routed_forms.registry:
            label = form[2]  # form registry is tuple (url, viewset, basename)
            name = self.form_names.get(label)
            if not name:
                logging.warning(
                    'Registered form %s without FormsInfo name provided, using label.', label)
                name = label
            available_forms.append({
                'label': label, 'name': name
            })
        return available_forms


forms_info_schema = {
    "200": openapi.Response(
        description="List of available forms.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="Email",
            properties={
                "label": openapi.Schema(
                    title="Form label",
                    type=openapi.TYPE_STRING,
                ),
                "name": openapi.Schema(
                    title="Form name",
                    type=openapi.TYPE_STRING,
                ),
            },
            required=["label", "name"],
        ),
        examples={
            "application/json": {
                "label": "customer_type",
                "name": "Customer Type"
            }
        }
    )
}


class FormsInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing forms. If permissions for specific forms will be added we
    should include it in here.
    """
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses=forms_info_schema)
    def list(self, request):
        forms_info = FormsInfo().get_available_forms()
        return Response(forms_info)
