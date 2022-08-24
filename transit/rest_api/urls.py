from django.urls import (
    include,
    path
)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

from transit.rest_api.forms.customer import CustomerViewSet
from transit.rest_api.forms.customer_type_master import CustomerTypeViewSet
from transit.rest_api.forms.delivery_status import DeliveryStatusViewSet
from transit.rest_api.forms.driver_master import DriverViewSet
from transit.rest_api.forms.item_details import ItemDetailsViewSet
from transit.rest_api.forms.item_master import ItemViewSet
from transit.rest_api.forms.mode_of_transport_master import ModeOfTransportViewSet
from transit.rest_api.forms.order_details import OrderDetailsViewSet, OrderLineDetailsViewSet
from transit.rest_api.forms.pod_variance import PODVarianceViewSet, PODVarianceDetailsViewSet
from transit.rest_api.forms.shipment import ShipmentDetailsViewSet
from transit.rest_api.forms.supplier_master import SupplierViewSet
from transit.rest_api.forms.transporter import TransporterViewSet
from transit.rest_api.forms.transporter_details import TransporterDetailsViewSet
from transit.rest_api.users import UserViewSet


# Routers provide an easy way of automatically determining the URL conf.

main_router = routers.DefaultRouter()
main_router.register(r'users', UserViewSet, basename='users')

forms_router = routers.DefaultRouter()
forms_router.register(r'customer_type', CustomerTypeViewSet, basename='customer_type')
forms_router.register(r'customer', CustomerViewSet, basename='customer')
forms_router.register(r'supplier', SupplierViewSet, basename='supplier')
forms_router.register(r'delivery_status', DeliveryStatusViewSet, basename='delivery_status')
forms_router.register(r'mode_of_transport', ModeOfTransportViewSet, basename='mode_of_transport')
forms_router.register(r'item', ItemViewSet, basename='item')
forms_router.register(r'item_details', ItemDetailsViewSet, basename='item_details')
forms_router.register(r'transporter', TransporterViewSet, basename='transporter')
forms_router.register(r'transporter_details', TransporterDetailsViewSet, basename='transporter_details')
forms_router.register(r'driver', DriverViewSet, basename='driver')
forms_router.register(r'order_details', OrderDetailsViewSet, basename='order_details')
forms_router.register(r'order_line_details', OrderLineDetailsViewSet, basename='order_line_details')
forms_router.register(r'shipment_details', ShipmentDetailsViewSet, basename='shipment_details')
forms_router.register(r'pod_variance', PODVarianceViewSet, basename='pod_variance')
forms_router.register(r'pod_variance_details', PODVarianceDetailsViewSet, basename='pod_variance_details')

main_router.registry.extend(forms_router.registry)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'api/', include((main_router.urls, 'transit'), namespace='API')),
]
