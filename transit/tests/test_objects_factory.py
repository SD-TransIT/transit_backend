from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, ClassVar, Type, Any

import django.db.models
from django.db import transaction

from transit.models import Supplier, CustomerType, ModeOfTransport, Item, ItemDetails, Driver, Transporter, \
    TransporterDetails, Customer, OrderDetails, OrderLineDetails, ShipmentDetails, DeliveryStatus, PODVariance, \
    PODVarianceDetails, CustomerWeekDays


@dataclass
class _FormModelFactory(ABC):
    _RELATED_MODEL_SEPARATOR = '__'
    model: ClassVar[Type[django.db.models.Model]]
    default_values: ClassVar[Dict[str, Any]]
    related_models_factories: ClassVar[Dict[str, "_FormModelFactory"]] = {}
    related_models_default_props: ClassVar[Dict[str, Any]] = {}
    custom_props: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.predefined_related_objects = self._get_predefined_related_models()
        self.related_objects_props = self._get_related_models_properties()
        self.related_without_definition = \
            set(self.related_models_factories.keys()) - set(self.predefined_related_objects)
        self.model_custom_values = {
            model: props for model, props in self.custom_props.items() if not self._has_related_model_prefix(model)
        }

    @transaction.atomic
    def create_object(self, save=True):
        related_objects = {
            **self.predefined_related_objects,
            **self._create_related_models(save=save)
        }
        model_inpatch = {**self.default_values, **related_objects, **self.model_custom_values}
        obj = self.model(**model_inpatch)
        if save:
            obj.save()
        return obj

    def _create_related_models(self, save=False):
        related_objects = {}
        for related_model in self.related_without_definition:
            props = {
                **self.related_models_default_props.get(related_model, {}),
                **self.related_objects_props.get(related_model, {})
            }
            next_obj = self.related_models_factories[related_model](custom_props=props).create_object(save=save)
            related_objects[related_model] = next_obj
        return related_objects

    def _get_related_models_properties(self):
        rel_props = defaultdict(lambda: dict())  # noqa: C408
        for key in self._get_related_fields_props():
            model, prop_name = key.split(self._RELATED_MODEL_SEPARATOR, maxsplit=1)
            rel_props[model][prop_name] = self.custom_props[key]
        return rel_props

    def _get_predefined_related_models(self):
        return {model: self.custom_props[model] for model in self._get_predefined_related_fields()}

    def _get_predefined_related_fields(self):
        # PK or Object explicitly provided
        relevant = self._get_related_fields_from_props()
        return [prop for prop in relevant if self._RELATED_MODEL_SEPARATOR not in prop]

    def _get_related_fields_props(self):
        # Partial information regarding new object provided
        relevant = self._get_related_fields_from_props()
        return [prop for prop in relevant if self._RELATED_MODEL_SEPARATOR in prop]

    def _get_related_fields_from_props(self):
        # Related models are defined through keys in related_model_factory
        return [prop for prop in self.custom_props.keys() if self._has_related_model_prefix(prop)]

    def _has_related_model_prefix(self, prop):
        # If prop name starts with related_model then true, e.g. item or item__name in ItemDetails
        return prop.split(self._RELATED_MODEL_SEPARATOR, maxsplit=1)[0] in self.related_models_factories


class CustomerTypeFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = CustomerType
    default_values: ClassVar[Dict] = {'customer_type_name': 'TestTypeNameBase'}


class DeliveryStatusFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = DeliveryStatus
    default_values: ClassVar[Dict] = {'delivery_status_key': 'delivered', 'delivery_status': 'Delivered'}


class CustomerFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = Customer
    related_models_factories = {'customer_type': CustomerTypeFactory}
    related_models_default_props = {'customer_type': {'customer_type_name': 'TestTypeNameBaseCustomer'}}
    default_values: ClassVar[Dict] = {
        'name': 'CustomerName', 'first_name': 'FirstCustomerName',
        'last_name': 'SecondTestName', 'phone': '123456789', 'email': 'e@mail.test'
    }


class CustomerWeekDaysFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = CustomerWeekDays
    related_models_factories = {'customer': CustomerFactory}
    related_models_default_props = {'customer__customer_type': {'customer_type_name': 'TypeForDaysCheck'}}
    default_values: ClassVar[Dict] = {
        'day': 1, 'opening_time': '10', 'closing_time': '18'
    }


class SupplierFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = Supplier
    default_values: ClassVar[Dict] = {
        'address_1': 'TestAddr1', 'address_2': 'TestAddr2', 'address_3': 'TestAddr3',
        'city': 'TestCity', 'state': 'TestState', 'country': 'TestCountry',
        'latitude_longitude': 'latitude_longitude:latitude_longitude',  # TODO: Change this to valid format
        'name': 'TestSupplier', 'phone': '123456789', 'email': 'supplier@mail.ad'
    }


class ModeOfTransportFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = ModeOfTransport
    default_values: ClassVar[Dict] = {
        'class_mode': 'TestClass', 'vehicle_type': 'TestVehicle'
    }


class ItemFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = Item
    default_values: ClassVar[Dict] = {
        'name': "ItemName", 'volume': 20.00, 'cost': 40.00,
        'weight': 50.00, 'category': 'ItemCategory',
        'sub_category': 'SubCategory', 'conditions': 'ColdChain'
    }


class ItemDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = ItemDetails
    related_models_factories = {'item': ItemFactory}
    related_models_default_props = {'item': {'name': 'ItemDetailsTestItemName'}}
    default_values: ClassVar[Dict] = {
        'expiry_date': datetime.now(tz=timezone.utc) + timedelta(days=1),
        'manufacturing_date': datetime(2022, 8, 17, tzinfo=timezone.utc),
        'received_date': datetime.now(tz=timezone.utc), 'gtin': 9999999, 'batch_number': "ItemDetailsBatch",
        'lot_number': "ItemDetailLot", 'serial_number': "ItemDetailSerial",
        'funding_source': "ItemDetailFundingSource"
    }


class TransporterFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = Transporter
    default_values: ClassVar[Dict] = {
        'address_1': 'TransportAddr1', 'address_2': 'TransportAddr2', 'address_3': 'TransportAddr3',
        'city': 'TransportCity', 'state': 'TransportState', 'country': 'TransportCountry',
        'latitude_longitude': 'latitude_longitude:latitude_longitude',
        'name': 'TestTransporter', 'phone': '987654321'
    }


class TransporterDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = TransporterDetails
    related_models_factories = {'transporter': TransporterFactory, 'mode_of_transport': ModeOfTransportFactory}
    related_models_default_props = {
        'transporter': {'name': 'DetailsTransporterNameTest'},
        'mode_of_transport': {'class_mode': "transporterClassMode", 'vehicle_type': 'TDTypeTest'}
    }
    default_values: ClassVar[Dict] = {
        'vehicle_number': '75192', 'vehicle_capacity_volume': '40', 'vehicle_capacity_weight': '70'
    }


class DriverFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = Driver
    related_models_factories = {'transporter': TransporterFactory}
    related_models_default_props = {'transporter': {'name': 'DriverTransporterTest'}}
    default_values: ClassVar[Dict] = {
        'name': 'Driver Name', 'username': 'DriverUsernameTest', 'password': 'DriverPassword'
    }


class OrderDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = OrderDetails
    related_models_factories = {'customer': CustomerFactory}
    related_models_default_props = {'customer': {'name': 'OrderDetailCustomerTest',
                                                 'customer_type__customer_type_name': 'TypeForOrder'}}
    default_values: ClassVar[Dict] = {'order_received_date': '2022-01-01'}


class OrderLineDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = OrderLineDetails
    related_models_factories = {
        'order_details': OrderDetailsFactory,
        'product': ItemFactory,  # In future product should be removed
        'item_details': ItemDetailsFactory,
    }
    related_models_default_props = {'item': {'name': 'ItemForOrderLineTest1'}}
    default_values: ClassVar[Dict] = {'quantity': '10'}


class ShipmentDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = ShipmentDetails
    related_models_factories = {
        'transporter_details': TransporterDetailsFactory,
        'driver': DriverFactory,
        'supplier': SupplierFactory,
        'delivery_status': DeliveryStatusFactory,
        'pod_status': DeliveryStatusFactory
    }
    related_models_default_props = {
        'transporter_details__transporter': {'name': 'NewShipTransporter'},
        'driver': {'name': 'Johan Strauss'},
        'supplier': {'name': 'ForShipmentSupplier'},
        'delivery_status': {'delivery_status_key': 'delivered1', 'delivery_status': 'Delivered1'},
        'pod_status': {'delivery_status_key': 'delivered2', 'delivery_status': 'Delivered2'}
    }
    default_values: ClassVar[Dict] = {
        'ship_date': datetime.now(tz=timezone.utc),
        'expected_delivery_date': datetime.now(tz=timezone.utc) + timedelta(days=1),
        'delivery_date': datetime.now(tz=timezone.utc) + timedelta(hours=20),
        'timestamp': datetime.now(tz=timezone.utc),
        'pod': True,
        'transporter_base_cost': 1000.00,
        'number_of_kilometers': 1000.00,
        'transporter_per_diem': 1000.00,
        'transporter_additional_cost': 150.00,
        'shipment_status': 1,
        'custom_route_number': '66',
        'gps_coordinates': 'str_for_coordinates',
        'description': 'Description',
        'ropo_number': '12',
        'signed_by': 'John Doe'
    }


class PODVarianceFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = PODVariance
    related_models_factories = {
        'shipment': ShipmentDetailsFactory
    }

    related_models_default_props = {'shipment__order_details': {'name': 'ForPODDetailsTest'},
                                    'shipment__item': {'name': 'ForPODItemTest'}}
    default_values: ClassVar[Dict] = {'dso_type': 'TestDSOforPOD'}


class PODVarianceDetailsFactory(_FormModelFactory):
    model: ClassVar[Type[django.db.models.Model]] = PODVarianceDetails
    related_models_factories = {
        'pod_variance': PODVarianceFactory,
        'order_line_details': OrderLineDetailsFactory,
    }
    related_models_default_props = {'order_line_details': {'quantity': '20'},
                                    'pod_variance': {'dso_type': 'Broken'}}
    default_values: ClassVar[Dict] = {'quantity': '15'}
