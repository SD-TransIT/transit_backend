import pandas as pd
from django.test import TestCase

from transit.tests.api_test.reports.utils import ReportTestCaseMixin


class TestReportCapacity(ReportTestCaseMixin, TestCase):
    _URL = 'orders_ready_to_be_shipped'

    def setUp(self):
        super(TestReportCapacity, self).setUp()
        self.complete_shipment.delivery_date = None
        self.complete_shipment.save()

    def expected_payload_complete(self):
        order_details_tuple = self.complete_shipment.order_mapping.first().order_details,
        order_details = order_details_tuple[0]
        return pd.DataFrame([{
            "row": 0,
            "ShipmentNumber": self.complete_shipment.id,
            "OrderNumber": order_details.order_details_id,
            "CustomerName": order_details.customer.name,
            "Address": order_details.customer.address_1,
            "Address2": order_details.customer.address_2,
            "Address3": order_details.customer.address_3,
            "City": order_details.customer.city,
            "Country": order_details.customer.country,
            "State": order_details.customer.state,
        }])

    def expected_payload_partial(self):
        order_details_tuple = self.partially_complete_shipment.order_mapping.first().order_details,
        order_details = order_details_tuple[0]
        return pd.DataFrame([{
            "row": 0,
            "ShipmentNumber": self.partially_complete_shipment.id,
            "OrderNumber": order_details.order_details_id,
            "CustomerName": order_details.customer.name,
            "Address": order_details.customer.address_1,
            "Address2": order_details.customer.address_2,
            "Address3": order_details.customer.address_3,
            "City": order_details.customer.city,
            "Country": order_details.customer.country,
            "State": order_details.customer.state,
        }])
