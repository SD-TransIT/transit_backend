from django.urls import (
    include,
    path
)

from transit.rest_api.reports.percent_capacity_utilization import PercentCapacityUtilizationView

urlpatterns = [
    path(
        r'percent_capacity_utilization/', PercentCapacityUtilizationView.as_view(), name='percent_capacity_utilization')
]
