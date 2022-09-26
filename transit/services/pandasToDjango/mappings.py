import random
import string
from datetime import datetime
from typing import List

import pandas
from django.db import models
from django.utils.translation import gettext_lazy as _
from pandas import DataFrame

from transit.models import Item, ItemDetails, Customer, OrderDetails, Supplier, OrderLineDetails, CustomerType
from transit.services.pandasToDjango.base import PandasToDjangoMappingAbs, PandasCellMappingDefinition, \
    PandasMappingException


class ItemMasterMapping(PandasToDjangoMappingAbs):
    model = Item
    excluded_fields = ['Item Code']
    mapping_definition = {
        'Name': PandasCellMappingDefinition(django_model_field='name'),
        'Category': PandasCellMappingDefinition(django_model_field='category'),
        'Sub Category': PandasCellMappingDefinition(django_model_field='sub_category'),
        'Volume': PandasCellMappingDefinition(django_model_field='volume'),
        'Weight': PandasCellMappingDefinition(django_model_field='weight'),
        'Cost': PandasCellMappingDefinition(django_model_field='cost'),
        'Is ColdChain': PandasCellMappingDefinition(
            django_model_field='conditions', mapping_function=lambda x: ItemMasterMapping._map_cold_chain(x))
    }

    @staticmethod
    def _map_cold_chain(cell_value):
        # TODO: ensure that Is ColdChain column is a boolean
        if cell_value is None:
            return Item.Condition.UNKNOWN
        elif cell_value:
            return Item.Condition.COLD_CHAIN
        else:
            return Item.Condition.AMBIENT


class CustomerDetailMapping(PandasToDjangoMappingAbs):
    model = Customer
    mapping_definition = {
        'Customer ID':
            PandasCellMappingDefinition('customer_type', lambda x: CustomerDetailMapping._customer_type(x)),
        'Name': PandasCellMappingDefinition('name'),
        'First Name': PandasCellMappingDefinition('first_name'),
        'Last Name': PandasCellMappingDefinition('last_name'),
        'Address 1': PandasCellMappingDefinition('address_1'),
        'Address 2': PandasCellMappingDefinition('address_2'),
        'Address 3': PandasCellMappingDefinition('address_3'),
        'City': PandasCellMappingDefinition('city'),
        'State': PandasCellMappingDefinition('state'),
        'Country': PandasCellMappingDefinition('country'),
        'Phone': PandasCellMappingDefinition('phone'),
        'Email': PandasCellMappingDefinition('email'),
        'LatitudeLongitude': PandasCellMappingDefinition('latitude_longitude'),
    }

    @staticmethod
    def _customer_type(customer_type_name):
        return CustomerType.objects.filter(customer_type_name=customer_type_name).get()


class ItemDetailMapping(PandasToDjangoMappingAbs):
    model = ItemDetails
    excluded_fields = ['Item Code']
    mapping_definition = {
        'Name': PandasCellMappingDefinition('item', lambda x: ItemDetailMapping._map_item_name_to_item(x)),
        'Batch Number': PandasCellMappingDefinition('batch_number'),
        'Expiry Date': PandasCellMappingDefinition('expiry_date'),
        'Date of Manufacture': PandasCellMappingDefinition('manufacturing_date'),
        'Date Received': PandasCellMappingDefinition('received_date'),
        'GTIN': PandasCellMappingDefinition('gtin'),
        'Lot Number': PandasCellMappingDefinition('lot_number'),
        'Serial Number': PandasCellMappingDefinition('serial_number'),
        'Funding Source': PandasCellMappingDefinition('funding_source'),
    }

    @staticmethod
    def _map_item_name_to_item(item_name):
        return Item.objects.get(name=item_name)

    @staticmethod
    def _map_date_field(date_value: str):
        """
        It's expected from dates to be provided in DD/MM/YYYY format.
        :param date_value: String representing date in format DD/MM/YYYY
        :return: datetime.date object
        """
        return datetime.strptime(date_value, "%d/%m/%Y")


class OrderLineDetailMapping(PandasToDjangoMappingAbs):
    """
    Additional mapping used during OrderDetails mapping on it's payload.
    """
    model = OrderLineDetails
    excluded_fields = [
        'Customer Order Number', 'Order Received Date (DD/MM/YYYY)',
        'Customer Name', 'Customer ID', 'Item Code'
    ]
    mapping_definition = {
        'Item Name': PandasCellMappingDefinition('product', lambda x: OrderLineDetailMapping._map_item_name_to_item(x)),
        'Quantity': PandasCellMappingDefinition('quantity')
    }

    def _map_pandas_row(self, row_data: pandas.Series) -> models.Model:
        """
        Order line detail has obligatory field item_details, however it's not a part of currently used xlsx payload.
        For now new item line detail is created where bulk number is constructed as
        random sequence of uppercase alphanumeric characters of length 10.
        """
        base = super(OrderLineDetailMapping, self)._map_pandas_row(row_data)
        batch_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        base.item_details = ItemDetails(batch_number=batch_number, item=base.product)
        return base

    @staticmethod
    def _map_item_name_to_item(item_name):
        return Item.objects.get(name=item_name)


class OrderDetailsMapping(PandasToDjangoMappingAbs):
    """
    This DataFrame provides information about both line items and order details. Therefore data is grouped by
    customer order number and customer. For every aggregation singe OrderDetail object is created, every row
    for given aggregation is mapped to line item with relation to OrderDetail.
    """
    model = OrderDetails
    excluded_fields = ['Item Code', 'Customer ID', 'Item Name', 'Quantity']
    mapping_definition = {
        'Customer Order Number': PandasCellMappingDefinition(
            'order_details_id', lambda x: OrderDetailsMapping._unique_order_detail_id(x)),
        'Order Received Date (DD/MM/YYYY)': PandasCellMappingDefinition('order_received_date'),
        'Customer Name': PandasCellMappingDefinition(
            'customer', lambda x: OrderDetailsMapping._map_customer_name_to_customer(x)),
    }

    line_details_mapping = OrderLineDetailMapping()

    def map_dataframe_to_django(self, pandas_rows: DataFrame) -> List[models.Model]:
        """
        As order provides information about both order and order line items its being handled in following
        way: DataFrame is grouped by OrderDetails properties and for every groping line items are created.
        Line items are added to django model as related field .line_items, however entities are not saved in db.
        """
        grouped = pandas_rows.groupby(['Customer Order Number', 'Order Received Date (DD/MM/YYYY)', 'Customer Name'])
        order_lines = [grouped.get_group(x) for x in grouped.groups]
        orders = []
        for order in order_lines:
            # This super() call is used to on groupby() product, therefore all elements would be the same.
            # Only one argument is taken.
            django_order = super(OrderDetailsMapping, self).map_dataframe_to_django(order[:1])[0]
            django_order.line_items_temp = self.line_details_mapping.map_dataframe_to_django(order)
            orders.append(django_order)
        return orders

    @staticmethod
    def _unique_order_detail_id(detail_id):
        if OrderDetails.objects.filter(order_details_id=detail_id).exists():
            raise PandasMappingException(message=(
                _('Customer Order Number %s already exist. Value has to be unique') % detail_id
            ))
        return detail_id

    @staticmethod
    def _map_customer_name_to_customer(customer_name):
        return Customer.objects.get(name=customer_name)


class SupplierMasterMapping(PandasToDjangoMappingAbs):
    model = Supplier
    excluded_fields = ['Supplier ID']
    mapping_definition = {
        'Name': PandasCellMappingDefinition('name'),
        'Address 1': PandasCellMappingDefinition('address_1'),
        'Address 2': PandasCellMappingDefinition('address_2'),
        'Address 3': PandasCellMappingDefinition('address_3'),
        'City': PandasCellMappingDefinition('city'),
        'State': PandasCellMappingDefinition('state'),
        'Country': PandasCellMappingDefinition('country'),
        'Phone': PandasCellMappingDefinition('phone'),
        'Email': PandasCellMappingDefinition('email'),
        'LatitudeLongitude': PandasCellMappingDefinition('latitude_longitude'),
    }
