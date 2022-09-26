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

from transit.rest_api.avaialble_froms_meta import FormsInfoViewSet
from transit.rest_api.forms_router import forms_router
from transit.rest_api.users import UserViewSet

# Routers provide an easy way of automatically determining the URL conf.

main_router = routers.DefaultRouter()
main_router.register(r'users', UserViewSet, basename='users')
main_router.register(r'available_forms', FormsInfoViewSet, basename='available_forms')
main_router.registry.extend(forms_router.registry)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'api/', include((main_router.urls, 'transit'), namespace='API')),
]
