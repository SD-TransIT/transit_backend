import datetime
import random
import string
import warnings
from datetime import timedelta

from django.db import transaction
from faker import Faker

from transit.models import Supplier, CustomerType, Customer, ModeOfTransport, Transporter, TransporterDetails, Driver, \
    Item, ItemDetails, OrderDetails, OrderLineDetails, ShipmentDetails, ShipmentOrderMapping, DeliveryStatus

fake = Faker('en_US')
fake2 = Faker(['en_GB'])


def email(free=False):
    if free:
        return {'email': fake.free_email()}
    else:
        return {'email': fake.company_email()}


def company_name():
    return {'name': fake.company()}


def phone():
    return {'phone': fake2.cellphone_number()}


def person_name():
    return {'name': fake.name()}


def address():
    lat_long = [float(x) for x in fake.latlng()]
    lat_long = F"({lat_long[0]}, {lat_long[1]})"
    return {
        'address_1': fake.address(), 'address_2': fake.address(),
        'address_3': fake.address(),
        'city': fake.city(), 'state': fake.state(),
        'country': 'USA',
        'latitude_longitude': lat_long
    }


def create_suppliers(number_=10):
    suppliers = []
    for _ in range(number_):
        supplier_data = {**address(), **email(), **company_name(), **phone()}
        suppliers.append(Supplier(**supplier_data))
    return suppliers


def create_customer_types():
    customer_types = []
    existing = CustomerType.objects.values_list('customer_type_name', flat=True)
    for name in ['Business', 'Private', 'Government']:
        if name not in existing:
            customer_types.append(CustomerType(**{'customer_type_name': name}))
    return customer_types


def create_customer(number_):
    available_types = ['Business', 'Private']
    customers = []
    for _ in range(number_):
        customer_type = available_types[random.randint(0, 1)]
        customer_data = {
            'customer_type': CustomerType.objects.filter(customer_type_name=customer_type).get(),
            **phone(),
        }
        if customer_type == 'Business':
            name = person_name()['name'].split(' ')[:2]
            first_name, last_name = name
            customer_data = {
                **customer_data, **company_name(),
                'first_name': first_name, 'last_name': last_name,
                **email()
            }
        elif customer_type == 'Private':
            name = person_name()
            name2 = name['name'].split(' ')[:2]
            first_name, last_name = name2
            customer_data = {
                **customer_data, **name,
                'first_name': first_name, 'last_name': last_name,
                **email(True)
            }

        customers.append(Customer(**customer_data))
    return customers


def create_mode_of_transports():
    expected = [
        {'class_mode': 'Air', 'vehicle_type': 'Plane'},
        {'class_mode': 'Ground', 'vehicle_type': 'Truck'},
        {'class_mode': 'Water', 'vehicle_type': 'Cargo Ship'},
    ]
    modes = []
    for expected_mode in expected:
        if not ModeOfTransport.objects.filter(**expected_mode).exists():
            modes.append(ModeOfTransport(**expected_mode))
    return modes


def create_delivery_status():
    for status in ['Delivered', 'Not Delivered', 'Unknown']:
        if not DeliveryStatus.objects.filter(delivery_status=status).exists():
            DeliveryStatus(delivery_status=status, delivery_status_key=status).save()


def create_transporters(numbers_):
    transporters = []
    for _ in range(numbers_):
        transporter_data = {
            **company_name(),
            **address(),
            **phone()
        }
        transporters.append(Transporter(**transporter_data))
    return transporters


def create_aircraft(type_):
    if type_ < 0 or type_ > 11:
        raise ValueError("Aircraft type out of range <0, 16>")
    allowed_aircrafts = [
      {
        "name": "Airbus A400M",
        "vehicle_capacity_volume": 270,
        "vehicle_capacity_weight": 37000
      },
      {
        "name": "Airbus A300-600F",
        "vehicle_capacity_volume": 391.4,
        "vehicle_capacity_weight": 48000
      },
      {
        "name": "Airbus A330-200F",
        "vehicle_capacity_volume": 475,
        "vehicle_capacity_weight": 70000
      },
      {
        "name": "Airbus A380[24]",
        "vehicle_capacity_volume": 342,
        "vehicle_capacity_weight": 68000
      },
      {
        "name": "Airbus Beluga",
        "vehicle_capacity_volume": 1210,
        "vehicle_capacity_weight": 47000
      },
      {
        "name": "Airbus BelugaXL",
        "vehicle_capacity_volume": 2615,
        "vehicle_capacity_weight": 53000
      },
      {
        "name": "Boeing 737-700C",
        "vehicle_capacity_volume": 107.6,
        "vehicle_capacity_weight": 18200
      },
      {
        "name": "Boeing 757-200F",
        "vehicle_capacity_volume": 239,
        "vehicle_capacity_weight": 39780
      },
      {
        "name": "Boeing 747-8F",
        "vehicle_capacity_volume": 854.5,
        "vehicle_capacity_weight": 134200
      },
      {
        "name": "Boeing 747 LCF",
        "vehicle_capacity_volume": 1840,
        "vehicle_capacity_weight": 83325
      },
      {"name": "Boeing 767-300F", "vehicle_capacity_volume": 438.2, "vehicle_capacity_weight": 52700},
      {"name": "Boeing 777F", "vehicle_capacity_volume": 653, "vehicle_capacity_weight": 103000},
    ]

    craft = allowed_aircrafts[type_]
    # Number in this case is name + salt
    craft['vehicle_number'] = craft.pop('name') + ' ' + ''.join(random.choices(string.ascii_uppercase, k=5))
    return craft


def create_truck(type_):
    if type_ < 0 or type_ > 5:
        raise ValueError("Aircraft type out of range <0, 5>")
    allowed = [
        {'name': 'GMC canyon', 'vehicle_capacity_volume': 1.2, 'vehicle_capacity_weight': 730},
        {'name': 'Ford F-150', 'vehicle_capacity_volume': 2.2, 'vehicle_capacity_weight': 1300},
        {'name': 'Nissan Titan', 'vehicle_capacity_volume': 3.4, 'vehicle_capacity_weight': 2200},
        {'name': 'International TerraStar', 'vehicle_capacity_volume': 12.0, 'vehicle_capacity_weight': 7200},
        {'name': 'Hino 600', 'vehicle_capacity_volume': 17.2, 'vehicle_capacity_weight': 13_000},
        {'name': 'Western Star 4800', 'vehicle_capacity_volume': 200.0, 'vehicle_capacity_weight': 120_000},
    ]

    craft = allowed[type_]
    # Number in this case is name + salt
    craft['vehicle_number'] = craft.pop('name') + ' ' + ''.join(random.choices(string.ascii_uppercase, k=5))
    return craft


def create_transporter_details(numbers_):
    allowed_types = list(ModeOfTransport.objects.filter(class_mode__in=['Air', 'Ground']))
    allowed_transporters = list(Transporter.objects.all())
    transport_details = []
    for _ in range(numbers_):
        type_ = allowed_types[random.randint(0, 1)]
        transporter = allowed_transporters[random.randint(0, len(allowed_transporters)-1)]
        if type_.class_mode == 'Air':
            details_data = {
                'transporter': transporter, 'mode_of_transport': type_,
                **create_aircraft(random.randint(0, 11))
            }
        elif type_.class_mode == 'Ground':
            details_data = {
                'transporter': transporter, 'mode_of_transport': type_,
                **create_truck(random.randint(0, 4))
            }
        else:
            raise ValueError(F"Invalid transport mode {type_}")
        transport_details.append(TransporterDetails(**details_data))
    return transport_details


def create_driver(numbers_):
    allowed_transporters = list(Transporter.objects.all())
    drivers = []
    for _ in range(numbers_):
        transporter = allowed_transporters[random.randint(0, len(allowed_transporters)-1)]
        driver_data = {'transporter': transporter, **person_name()}
        drivers.append(Driver(**driver_data))
    return drivers


def create_item():
    items = [
        {'name': 'Pills Type 1, 100 small tablets', 'weight': 0.3, 'volume': (1.2/1000) , 'cost': 65.0, 'category': 'PILLS'},
        {'name': 'Pills Type 2, 100 large tablets', 'weight': 0.8, 'volume': (2.4/1000) , 'cost': 120.5, 'category': 'PILLS'},
        {'name': 'Pills Type 3, 100 small tablets', 'weight': 0.3, 'volume': (1.2/1000) , 'cost': 99.0, 'category': 'PILLS'},
        {'name': 'Ampoules 1, 100 amp. 5ml', 'weight': 1.0, 'volume': (2.2/1000) , 'cost': 99.0, 'category': 'AMPOULES'},
        {'name': 'Ampoules 2, 100 amp. 10ml', 'weight': 1.6, 'volume': (3.5/1000) , 'cost': 420.45, 'category': 'AMPOULES'},
        {'name': 'Ampoules 2, 100 amp. 10ml', 'weight': 1.6, 'volume': (3.5/1000) , 'cost': 1200.00, 'category': 'AMPOULES'},
        {'name': 'Syringes 1, 100 syringes, 5ml', 'weight': 1.0, 'volume': (9.0/1000) , 'cost': 15.0, 'category': 'SYRINGES'},
        {'name': 'Syringes 2, 100 syringes, 10ml', 'weight': 1.6, 'volume': (12.0/1000) , 'cost': 23.0, 'category': 'SYRINGES'},
        {'name': '10 Elastic Bandages', 'weight': 0.2, 'volume': (1.8/1000) , 'cost': 55.00, 'category': 'GLOVES'},
        {'name': 'Gloves, 100 pairs', 'weight': 5, 'volume': (35.0/1000) , 'cost': 16.00, 'category': 'GLOVES'},
    ]
    items_create = []
    for item in items:
        if not Item.objects.filter(**item).exists():
            items_create.append(Item(**item))
    return items_create


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_item_details(numbers_):
    all_items = list(Item.objects.all())
    item_details = []
    for _ in range(numbers_):
        item = all_items[random.randint(0, len(all_items)-1)]
        manufacture = random_date(datetime.date(2018, 1, 1), datetime.date(2022, 9, 30))
        expire = random_date(manufacture+timedelta(days=360), datetime.date(2023, 12, 30)+timedelta(days=700))
        received_date = random_date(manufacture+timedelta(days=10), manufacture+timedelta(days=360))

        item_details_data = {
            'batch_number': "".join(random.choices(string.ascii_uppercase+string.digits, k=10)),
            'manufacturing_date': manufacture,
            'expiry_date': expire,
            'received_date': received_date,
            'gtin': random.randint(1000, 999999),
            'item': item
        }
        item_details.append(ItemDetails(**item_details_data))
    return item_details


def create_orders(number_):
    orders = []

    for _ in range(number_):
        rec_date = random_date(datetime.date(2022, 1, 1), datetime.date(2022, 9, 30))
        order_data = {
            'customer': Customer.objects.order_by('?').first(),  # Random,
            'order_received_date': None if random.randint(0, 2) == 0 else rec_date
        }
        ord = OrderDetails(**order_data)
        orders.append(ord)
        #ord.save()

    OrderDetails.objects.bulk_create(orders)
    line_items = []
    for i, o in enumerate(orders):
        if not ItemDetails.objects.filter(order_line_item__isnull=True).count() < 7:
            # Add items if none available
            items = create_item_details(10)
            ItemDetails.objects.bulk_create(items)

        for _ in range(random.randint(1, 7)):
            item = ItemDetails.objects.filter(order_line_item__isnull=True).order_by('?').first()
            order_line_items = {
                'order_details': o, 'item_details': item,
                'product': item.item, 'quantity': random.randint(1, 20)
            }
            line_items.append(OrderLineDetails(**order_line_items))

    OrderLineDetails.objects.bulk_create(line_items)
    return orders


def create_shipments(number_):
    shipments = []
    order_lines = []

    for n in range(number_):
        transporter = Transporter.objects.filter(vehicles__isnull=False, drivers__isnull=False).order_by('?').first()
        trahsporter_vehicle = transporter.vehicles.all().order_by('?').first()
        shipment_date = random_date(datetime.date(2021, 1, 1), datetime.date(2022, 9, 30))
        expected_delivery_date = random_date(shipment_date + datetime.timedelta(days=10), datetime.date(2023, 9, 30))
        delivery_date = expected_delivery_date

        if random.randint(0, 10) == 0:
            shipment_date, expected_delivery_date, delivery_date = None, None, None
        elif random.randint(0, 5) == 0:
            delivery_date = random_date(expected_delivery_date + datetime.timedelta(days=10),
                                        datetime.date(2023, 12, 30))

        number_of_kilometers = random.randint(10, 10_000)
        transporter_base_cost = random.randint(400, 900)*10.0
        transporter_per_diem = random.randint(400, 900)*10.0
        transporter_additional_cost = random.randint(400, 900)*10.0

        shipment_data = {
            'transporter_details': trahsporter_vehicle,
            'driver': transporter.drivers.all().order_by('?').first(),
            'supplier': Supplier.objects.all().order_by('?').first(),
            'ship_date': shipment_date,
            'expected_delivery_date': expected_delivery_date,
            'delivery_date': delivery_date,
            'number_of_kilometers': number_of_kilometers,
            'transporter_base_cost': transporter_base_cost,
            'transporter_per_diem': transporter_per_diem,
            'transporter_additional_cost': transporter_additional_cost,
            'delivery_status': DeliveryStatus.objects.order_by('?').first(),
            'pod_status': DeliveryStatus.objects.order_by('?').first(),
            'shipment_status': random.randint(0, 3)
        }

        orders = random.randint(1, int(float(trahsporter_vehicle.vehicle_capacity_volume))+1)
        if orders > 20:
            orders = 20
        if OrderDetails.objects.without_shipment_details().count() < orders:
            create_orders(orders*10)
        shipment = ShipmentDetails(**shipment_data)
        shipment.save()
        som = []
        for _ in range(random.randint(0, orders)):
            order = OrderDetails.objects.without_shipment_details().order_by('?').first()
            mapping = ShipmentOrderMapping(shipment_details=shipment, order_details=order)
            som.append(mapping)
        ShipmentOrderMapping.objects.bulk_create(som)
        if n%10 == 0:
            print(f"Shipment progress {n}/{number_}.")
    return shipments


@transaction.atomic
def build_database_info(n):
    create_delivery_status()
    s = create_suppliers(n*10)
    Supplier.objects.bulk_create(s)
    c_t = create_customer_types()
    CustomerType.objects.bulk_create(c_t)
    print('Supplier added')
    c = create_customer(n*10)
    Customer.objects.bulk_create(c)
    print('Customer added')
    mot = create_mode_of_transports()
    ModeOfTransport.objects.bulk_create(mot)
    t = create_transporters(n*10)
    Transporter.objects.bulk_create(t)
    td = create_transporter_details(n)
    print('Transporters added')
    TransporterDetails.objects.bulk_create(td)
    d = create_driver(n*10)
    Driver.objects.bulk_create(d)
    print('Drivers added')
    i = create_item()
    Item.objects.bulk_create(i)
    id_ = create_item_details(n*10)
    print('Item Details added')
    ItemDetails.objects.bulk_create(id_)
    orders = create_orders(n)
    print('Orders added')
    shipments = create_shipments(n)
    print('Shipments added')


with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    build_database_info(100)
