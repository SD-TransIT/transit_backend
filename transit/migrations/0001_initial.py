# Generated by Django 4.0.6 on 2022-08-10 08:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('address_1', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, db_column='Address2', max_length=255, null=True)),
                ('address_3', models.CharField(blank=True, db_column='Address3', max_length=255, null=True)),
                ('city', models.CharField(blank=True, db_column='City', max_length=255, null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('country', models.CharField(blank=True, db_column='Country', max_length=255, null=True)),
                ('latitude_longitude', models.CharField(blank=True, db_column='LatitudeLongitude', max_length=255, null=True)),
                ('customer_name', models.CharField(db_column='CustomerName', max_length=255)),
                ('first_name', models.CharField(blank=True, db_column='FirstName', max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, db_column='LastName', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Customer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('customer_type_name', models.CharField(blank=True, db_column='CustomerTypeName', max_length=255, null=True)),
            ],
            options={
                'db_table': 'CustomerType',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('delivery_status_key', models.CharField(db_column='DeliveryStatusKey', max_length=50, primary_key=True, serialize=False, unique=True)),
                ('delivery_status', models.CharField(db_column='DeliveryStatus', max_length=50)),
            ],
            options={
                'db_table': 'DeliveryStatus',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('driver_name', models.CharField(db_column='DriverName', max_length=255)),
                ('username', models.CharField(blank=True, db_column='Username', max_length=50, null=True)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=50, null=True)),
            ],
            options={
                'db_table': 'Driver',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('composite_product_name', models.CharField(blank=True, db_column='CompositeProductName', max_length=255, null=True)),
                ('volume', models.DecimalField(blank=True, db_column='volume', decimal_places=2, max_digits=18, null=True)),
                ('cost', models.DecimalField(blank=True, db_column='Cost', decimal_places=2, max_digits=18, null=True)),
                ('weight', models.DecimalField(blank=True, db_column='Weight', decimal_places=2, max_digits=18, null=True)),
                ('category', models.CharField(blank=True, db_column='Category', max_length=255, null=True)),
                ('sub_category', models.CharField(blank=True, db_column='SubCategory', max_length=255, null=True)),
                ('conditions', models.CharField(blank=True, db_column='Conditions', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Item',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('expiry_date', models.DateTimeField(blank=True, db_column='ExpiryDate', null=True)),
                ('manufacturing_date', models.DateTimeField(blank=True, db_column='ManufacturingDate', null=True)),
                ('received_date', models.DateTimeField(blank=True, db_column='ReceivedDate', null=True)),
                ('gtin', models.BigIntegerField(blank=True, db_column='GTIN', null=True)),
                ('batch_number', models.CharField(blank=True, db_column='BatchNumber', max_length=255, null=True)),
                ('lot_number', models.CharField(blank=True, db_column='LotNumber', max_length=255, null=True)),
                ('serial_number', models.CharField(blank=True, db_column='SerialNumber', max_length=255, null=True)),
                ('funding_source', models.CharField(blank=True, db_column='FundingSource', max_length=255, null=True)),
                ('item_product', models.ForeignKey(db_column='ItemID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.item')),
            ],
            options={
                'db_table': 'ItemDetails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ModeOfTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('class_mode', models.CharField(blank=True, db_column='Class', max_length=255, null=True)),
                ('vehicle_type', models.CharField(blank=True, db_column='VehicleType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'ModeOfTransport',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('order_details_id', models.CharField(db_column='OrderDetailsID', max_length=50, primary_key=True, serialize=False, unique=True)),
                ('order_received_date', models.CharField(blank=True, db_column='OrderReceivedDate', max_length=255, null=True)),
                ('customer', models.ForeignKey(db_column='CustomerID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.customer')),
            ],
            options={
                'db_table': 'OrderDetails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderLineDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('quantity', models.DecimalField(blank=True, db_column='Quantity', decimal_places=2, max_digits=18, null=True)),
                ('old_quantity', models.DecimalField(blank=True, db_column='OldQuantity', decimal_places=2, max_digits=18, null=True)),
                ('item_details', models.ForeignKey(db_column='ItemDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.itemdetails')),
                ('order_details', models.ForeignKey(db_column='OrderDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.orderdetails')),
                ('product', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.item')),
            ],
            options={
                'db_table': 'OrderLineDetails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('status', models.CharField(db_column='Status', max_length=255)),
            ],
            options={
                'db_table': 'OrderStatus',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PODVariance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('dso_type', models.CharField(blank=True, db_column='DSOType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'PODVariance',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PortalAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('username', models.CharField(blank=True, db_column='UserName', max_length=50, null=True)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=50, null=True)),
                ('role', models.CharField(blank=True, db_column='Role', max_length=50, null=True)),
                ('region', models.CharField(blank=True, db_column='Region', max_length=255, null=True)),
            ],
            options={
                'db_table': 'PortalAccess',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ShipmentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('ship_date', models.DateTimeField(blank=True, db_column='ShipDate', null=True)),
                ('expected_delivery_date', models.DateTimeField(blank=True, db_column='ExpectedDeliveryDate', null=True)),
                ('delivery_date', models.DateTimeField(blank=True, db_column='DeliveryDate', null=True)),
                ('timestamp', models.DateTimeField(blank=True, db_column='Timestamp', null=True)),
                ('pod', models.BooleanField(blank=True, db_column='POD', null=True)),
                ('delay_justified', models.BooleanField(blank=True, db_column='DelayJustified', null=True)),
                ('transporter_base_cost', models.DecimalField(blank=True, db_column='TransporterBaseCost', decimal_places=2, max_digits=18, null=True)),
                ('number_of_kilometers', models.DecimalField(blank=True, db_column='NumberOfKilometers', decimal_places=2, max_digits=18, null=True)),
                ('transporter_per_diem', models.DecimalField(blank=True, db_column='TransporterPerDiem', decimal_places=2, max_digits=18, null=True)),
                ('transporter_additional_cost', models.DecimalField(blank=True, db_column='TransporterAdditionalCost', decimal_places=2, max_digits=18, null=True)),
                ('shipment_status', models.IntegerField(blank=True, db_column='ShipmentStatus', null=True)),
                ('custom_route_number', models.CharField(blank=True, db_column='CustomRouteNumber', max_length=50, null=True)),
                ('gps_coordinates', models.CharField(blank=True, db_column='GPSCoordinates', max_length=50, null=True)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=50, null=True)),
                ('ropo_number', models.CharField(blank=True, db_column='ROPONumber', max_length=255, null=True)),
                ('signed_by', models.CharField(blank=True, db_column='SignedBy', max_length=255, null=True)),
                ('delivery_status', models.ForeignKey(db_column='DeliveryStatus', on_delete=django.db.models.deletion.DO_NOTHING, related_name='delivery_status_master', to='transit.deliverystatus')),
                ('driver', models.ForeignKey(db_column='DriverID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.driver')),
                ('pod_status', models.ForeignKey(db_column='PODStatus', on_delete=django.db.models.deletion.DO_NOTHING, related_name='delivery_status_master1', to='transit.deliverystatus')),
            ],
            options={
                'db_table': 'ShipmentDetails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('address_1', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, db_column='Address2', max_length=255, null=True)),
                ('address_3', models.CharField(blank=True, db_column='Address3', max_length=255, null=True)),
                ('city', models.CharField(blank=True, db_column='City', max_length=255, null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('country', models.CharField(blank=True, db_column='Country', max_length=255, null=True)),
                ('latitude_longitude', models.CharField(blank=True, db_column='LatitudeLongitude', max_length=255, null=True)),
                ('transporter_name', models.CharField(db_column='TransporterName', max_length=255)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Transporter',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TransporterDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('vehicle_number', models.CharField(blank=True, db_column='VehicleNumber', max_length=255, null=True)),
                ('vehicle_capacity_volume', models.CharField(blank=True, db_column='VehicleCapacityVolume', max_length=255, null=True)),
                ('vehicle_capacity_weight', models.CharField(blank=True, db_column='VehicleCapacityWeight', max_length=255, null=True)),
                ('mode_of_transport', models.ForeignKey(db_column='ModeOfTransportID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.modeoftransport')),
                ('transporter', models.ForeignKey(db_column='TransporterID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.transporter')),
            ],
            options={
                'db_table': 'TransporterDetails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('address_1', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, db_column='Address2', max_length=255, null=True)),
                ('address_3', models.CharField(blank=True, db_column='Address3', max_length=255, null=True)),
                ('city', models.CharField(blank=True, db_column='City', max_length=255, null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('country', models.CharField(blank=True, db_column='Country', max_length=255, null=True)),
                ('latitude_longitude', models.CharField(blank=True, db_column='LatitudeLongitude', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Supplier',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ShipmentOrderMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('order_details', models.ForeignKey(db_column='OrderDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.orderdetails')),
                ('shipment_details', models.ForeignKey(db_column='ShipmentDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.shipmentdetails')),
            ],
            options={
                'db_table': 'ShipmentOrderMapping',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='shipmentdetails',
            name='supplier',
            field=models.ForeignKey(db_column='SupplierID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.supplier'),
        ),
        migrations.AddField(
            model_name='shipmentdetails',
            name='transporter_details',
            field=models.ForeignKey(db_column='TransporterDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.transporterdetails'),
        ),
        migrations.CreateModel(
            name='PODVarianceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(db_column='LastModifiedDate', default=datetime.datetime.now)),
                ('last_modified_by', models.CharField(db_column='LastModifiedBy', max_length=255)),
                ('quantity', models.DecimalField(db_column='Quantity', decimal_places=2, max_digits=18)),
                ('order_line_details', models.ForeignKey(db_column='OrderLineDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.orderlinedetails')),
                ('pod_variance', models.ForeignKey(db_column='PODVarianceID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.podvariance')),
            ],
            options={
                'db_table': 'PODVarianceDetails',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='podvariance',
            name='shipment',
            field=models.ForeignKey(db_column='ShipmentID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.shipmentdetails'),
        ),
        migrations.AddField(
            model_name='driver',
            name='transporter',
            field=models.ForeignKey(db_column='TransporterID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.transporter'),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_type',
            field=models.ForeignKey(db_column='CustomerTypeID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.customertype'),
        ),
        migrations.CreateModel(
            name='CustomerWeekDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(db_column='Day')),
                ('opening_time', models.CharField(db_column='OpeningTime', max_length=50)),
                ('closing_time', models.CharField(db_column='ClosingTime', max_length=50)),
                ('closed', models.BooleanField(blank=True, db_column='Closed', default=False, null=True)),
                ('meridiem_indicator_opening_time', models.CharField(blank=True, db_column='Meridiem_Indicator_OpeningTime', max_length=20, null=True)),
                ('meridiem_indicator_closing_time', models.CharField(blank=True, db_column='Meridiem_Indicator_ClosingTime', max_length=20, null=True)),
                ('customer', models.ForeignKey(db_column='CustomerID', on_delete=django.db.models.deletion.DO_NOTHING, to='transit.customer')),
            ],
            options={
                'db_table': 'CustomerWeekDays',
                'managed': True,
            },
        ),
    ]