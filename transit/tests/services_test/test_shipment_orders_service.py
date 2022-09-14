from django.test import TestCase
from rest_framework import serializers

from transit.models import ShipmentOrderMapping
from transit.services.shipment_orders_service import ShipmentOrdersService
from transit.tests.test_objects_factory import ShipmentDetailsFactory, OrderDetailsFactory, CustomerFactory


class TestShipmentOrderService(TestCase):

    def setUp(self):
        super(TestShipmentOrderService, self).setUp()
        self._test_shipment = ShipmentDetailsFactory().create_object(True)
        self._test_order_customer1 = OrderDetailsFactory(custom_props={
            'order_details_id': 'CharID1',
            'customer': CustomerFactory(custom_props={
                'name': 'OrderDetailCustomerTest',
                'customer_type__customer_type_name': 'TypeForOrder1'
            }).create_object(True)
        }).create_object()

        self._test_order2_customer1 = OrderDetailsFactory(custom_props={
            'customer': self._test_order_customer1.customer, 'order_details_id': 'CharID2'
        }).create_object()

        self._test_order_customer2 = OrderDetailsFactory(custom_props={
            'order_details_id': 'CharID3',
            'customer': CustomerFactory(custom_props={
                'name': 'OrderDetailCustomerTest1',
                'customer_type__customer_type_name': 'TypeForOrder2'
            }).create_object(True)
        }).create_object(True)

    def test_create_ok(self):
        service = ShipmentOrdersService()
        service.create(
            shipment=self._test_shipment,
            orders=[self._test_order_customer1, self._test_order2_customer1]
        )
        self.assertEqual(
            ShipmentOrderMapping.objects.filter(
                shipment_details=self._test_shipment,
                order_details__in=[self._test_order_customer1, self._test_order2_customer1]).count(), 2
        )

    def test_create_multiple_customers(self):
        service = ShipmentOrdersService()
        expected_error = "All orders assigned to order have to be assigned to same customers. " \
                         "Provided orders are assigned to multiple customers: .*"
        with self.assertRaisesRegex(serializers.ValidationError, expected_error):
            service.create(
                shipment=self._test_shipment,
                orders=[self._test_order_customer1, self._test_order_customer2]
            )

    def test_create_order_with_shipment(self):
        service = ShipmentOrdersService()
        service.create(self._test_shipment, [self._test_order_customer1])
        with self.assertRaisesRegex(serializers.ValidationError,
                                    "Some of provided shipment details already assigned to shipment: .*"):
            service.create(self._test_shipment, [self._test_order_customer1])

    def test_update_multiple_customers(self):
        service = ShipmentOrdersService()
        expected_error = "All orders assigned to order have to be assigned to same customers. " \
                         "Provided orders are assigned to multiple customers: .*"
        with self.assertRaisesRegex(serializers.ValidationError,expected_error):
            service.create(
                shipment=self._test_shipment,
                orders=[self._test_order_customer1, self._test_order_customer2]
            )

    def test_update_ok_remove_not_lister(self):
        service = ShipmentOrdersService()
        service.create(
            shipment=self._test_shipment,
            orders=[self._test_order2_customer1]
        )
        service.update(
            shipment=self._test_shipment,
            orders=[self._test_order_customer1]
        )

        self.assertFalse(
            ShipmentOrderMapping.objects.filter(
                shipment_details=self._test_shipment, order_details=self._test_order2_customer1).exists()
        )
        self.assertTrue(
            ShipmentOrderMapping.objects.filter(
                shipment_details=self._test_shipment, order_details=self._test_order_customer1).exists()
        )

    def test_update_ok_one_existing_one_new(self):
        service = ShipmentOrdersService()
        service.create(
            shipment=self._test_shipment,
            orders=[self._test_order2_customer1]
        )
        service.update(
            shipment=self._test_shipment,
            orders=[self._test_order2_customer1, self._test_order_customer1]
        )

        self.assertTrue(
            ShipmentOrderMapping.objects.filter(
                shipment_details=self._test_shipment, order_details=self._test_order2_customer1).exists()
        )
        self.assertTrue(
            ShipmentOrderMapping.objects.filter(
                shipment_details=self._test_shipment, order_details=self._test_order_customer1).exists()
        )
