# Generated by Django 4.0.6 on 2022-09-08 11:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transit', '0006_alter_shipmentdetailfiles_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='customertype',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='driver',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='item',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='itemdetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='modeoftransport',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderlinedetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='podvariance',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='podvariance',
            name='shipment',
            field=models.ForeignKey(db_column='ShipmentID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='pod_variances', to='transit.shipmentdetails'),
        ),
        migrations.AlterField(
            model_name='podvariancedetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='portalaccess',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shipmentdetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shipmentordermapping',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shipmentordermapping',
            name='order_details',
            field=models.ForeignKey(db_column='OrderDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipment_mapping', to='transit.orderdetails'),
        ),
        migrations.AlterField(
            model_name='shipmentordermapping',
            name='shipment_details',
            field=models.ForeignKey(db_column='ShipmentDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_mapping', to='transit.shipmentdetails'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transporter',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transporterdetails',
            name='last_modified_date',
            field=models.DateTimeField(db_column='LastModifiedDate', default=django.utils.timezone.now),
        ),
    ]