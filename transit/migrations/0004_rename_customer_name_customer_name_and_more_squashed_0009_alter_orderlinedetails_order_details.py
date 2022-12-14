# Generated by Django 4.0.6 on 2022-08-22 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('transit', '0004_rename_customer_name_customer_name_and_more'), ('transit', '0005_alter_itemdetails_item'), ('transit', '0006_rename_driver_name_driver_name_and_more'), ('transit', '0007_alter_deliverystatus_delivery_status_key'), ('transit', '0008_alter_orderdetails_order_details_id'), ('transit', '0009_alter_orderlinedetails_order_details')]

    dependencies = [
        ('transit', '0003_formsclerk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='composite_product_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='itemdetails',
            old_name='item_product',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='transporter',
            old_name='transporter_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='supplier',
            name='name',
            field=models.CharField(db_column='Name', default='UNDEFINED', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customertype',
            name='customer_type_name',
            field=models.CharField(blank=True, db_column='CustomerTypeName', max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='conditions',
            field=models.CharField(choices=[('', ''), ('ColdChain', 'Cold Chain'), ('Ambient', 'Ambient')], db_column='Conditions', default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemdetails',
            name='batch_number',
            field=models.CharField(db_column='BatchNumber', default='UNDEFINED', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderlinedetails',
            name='old_quantity',
            field=models.DecimalField(db_column='OldQuantity', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='orderlinedetails',
            name='quantity',
            field=models.DecimalField(db_column='Quantity', decimal_places=2, default=0, max_digits=18),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemdetails',
            name='item',
            field=models.ForeignKey(db_column='ItemID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_details', to='transit.item'),
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='driver_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='delivery_date',
            field=models.DateTimeField(db_column='DeliveryDate', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='expected_delivery_date',
            field=models.DateTimeField(db_column='ExpectedDeliveryDate', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='number_of_kilometers',
            field=models.DecimalField(db_column='NumberOfKilometers', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='pod',
            field=models.BooleanField(db_column='POD', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='ship_date',
            field=models.DateTimeField(db_column='ShipDate', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='timestamp',
            field=models.DateTimeField(db_column='Timestamp', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='transporter_additional_cost',
            field=models.DecimalField(db_column='TransporterAdditionalCost', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='transporter_base_cost',
            field=models.DecimalField(db_column='TransporterBaseCost', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='transporter_per_diem',
            field=models.DecimalField(db_column='TransporterPerDiem', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='deliverystatus',
            name='delivery_status_key',
            field=models.CharField(db_column='DeliveryStatusKey', max_length=64, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order_details_id',
            field=models.CharField(db_column='OrderDetailsID', max_length=64, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='orderlinedetails',
            name='order_details',
            field=models.ForeignKey(db_column='OrderDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='line_items', to='transit.orderdetails'),
        ),
    ]
