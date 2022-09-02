from rest_framework import routers

from transit.rest_api.forms.customer import CustomerViewSet
from transit.rest_api.forms.customer_type_master import CustomerTypeViewSet
from transit.rest_api.forms.delivery_status import DeliveryStatusViewSet
from transit.rest_api.forms.driver_master import DriverViewSet
from transit.rest_api.forms.item_details import ItemDetailsViewSet
from transit.rest_api.forms.item_master import ItemViewSet
from transit.rest_api.forms.mode_of_transport_master import ModeOfTransportViewSet
from transit.rest_api.forms.order_details import OrderDetailsViewSet, OrderLineDetailsViewSet
from transit.rest_api.forms.pod_variance import PODVarianceViewSet, PODVarianceDetailsViewSet
from transit.rest_api.forms.shipment import ShipmentDetailsViewSet, ShipmentDetailFilesViewSet
from transit.rest_api.forms.supplier_master import SupplierViewSet
from transit.rest_api.forms.transporter import TransporterViewSet
from transit.rest_api.forms.transporter_details import TransporterDetailsViewSet


def manual_forms() -> routers.DefaultRouter:
    router = routers.DefaultRouter()
    router.register(r'supplier', SupplierViewSet, basename='supplier')
    router.register(r'customer_type', CustomerTypeViewSet, basename='customer_type')
    router.register(r'customer', CustomerViewSet, basename='customer')
    router.register(r'mode_of_transport', ModeOfTransportViewSet, basename='mode_of_transport')
    router.register(r'item', ItemViewSet, basename='item')
    router.register(r'item_details', ItemDetailsViewSet, basename='item_details')
    router.register(r'transporter_details', TransporterDetailsViewSet, basename='transporter_details')
    router.register(r'driver', DriverViewSet, basename='driver')
    router.register(r'order_details', OrderDetailsViewSet, basename='order_details')
    router.register(r'shipment_details', ShipmentDetailsViewSet, basename='shipment_details')
    router.register(r'cost', ShipmentDetailsViewSet, basename='cost')
    router.register(r'pod_variance', PODVarianceViewSet, basename='pod_variance')
    return router


def manual_forms_extra():
    router = routers.DefaultRouter()
    router.register(r'delivery_status', DeliveryStatusViewSet, basename='delivery_status')
    router.register(r'transporter', TransporterViewSet, basename='transporter')
    router.register(r'order_line_details', OrderLineDetailsViewSet, basename='order_line_details')
    router.register(r'pod_variance_details', PODVarianceDetailsViewSet, basename='pod_variance_details')
    router.register(r'shipment_details_files', ShipmentDetailFilesViewSet, basename='shipment_details_files')
    return router


def assemble_build_router():
    router = routers.DefaultRouter()
    router.registry.extend(manual_forms().registry)
    router.registry.extend(manual_forms_extra().registry)
    return router


forms_router = assemble_build_router()