import datetime

import pandas as pd
from django.test import TestCase

from transit.models import DeliveryStatus, PODVariance, ShipmentOrderMapping, OrderLineDetails
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.api_test.reports.utils import ReportTestCaseMixin
from transit.tests.test_objects_factory import ShipmentDetailsFactory, DeliveryStatusFactory, OrderLineDetailsFactory


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'number_of_damaged_short_over_shipments'

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        ship_date_3 = datetime.datetime(year=2021, month=8, day=1, tzinfo=datetime.timezone.utc)
        self.shipment3 = ShipmentDetailsFactory(custom_props={'ship_date': ship_date_3}).create_object(True)
        pod_variance = PODVariance(shipment=self.shipment3, dso_type=PODVariance.DSOType.DAMAGED.name)
        pod_variance.save()
        ShipmentOrderMapping.objects.filter(order_details=self.order_line_detail.order_details).delete()
        service = ShipmentOrdersService()
        self.order_line_detail.old_quantity = 5.0
        self.order_line_detail.save()
        print(list(OrderLineDetails.objects.values_list('old_quantity')))
        service.add_orders_to_shipment(shipment=self.shipment3, orders=[self.order_line_detail.order_details])

    def expected_payload(self):
        return pd.DataFrame([{
            "row": 0,
            "ShipDate": datetime.date(year=2021, month=8, day=1),
            "TransporterName": self.shipment.transporter_details.transporter.name,
            "VehicleNumber": self.shipment.transporter_details.vehicle_number,
            "CustomRouteNumber": "66",
            "DSOType": 'DAMAGED',
            "OldQuantity": 5.0,
            "NewQuantity": 10.0,
        }])
