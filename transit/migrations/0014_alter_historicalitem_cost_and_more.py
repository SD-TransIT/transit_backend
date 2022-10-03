# Generated by Django 4.0.6 on 2022-10-01 16:25

from django.db import migrations, models
import django.db.models.deletion
import transit.models.order_details


class Migration(migrations.Migration):

    dependencies = [
        ('transit', '0013_alter_historicalorderdetails_order_details_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalitem',
            name='cost',
            field=models.DecimalField(blank=True, db_column='Cost', decimal_places=5, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='historicalitem',
            name='volume',
            field=models.DecimalField(blank=True, db_column='volume', decimal_places=5, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='historicalorderdetails',
            name='order_details_id',
            field=models.CharField(db_column='OrderDetailsID', db_index=True, default=transit.models.order_details._default_order_details_id, max_length=64),
        ),
        migrations.AlterField(
            model_name='item',
            name='cost',
            field=models.DecimalField(blank=True, db_column='Cost', decimal_places=5, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='volume',
            field=models.DecimalField(blank=True, db_column='volume', decimal_places=5, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order_details_id',
            field=models.CharField(db_column='OrderDetailsID', default=transit.models.order_details._default_order_details_id, max_length=64, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='orderlinedetails',
            name='item_details',
            field=models.ForeignKey(db_column='ItemDetailsID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_line_item', to='transit.itemdetails'),
        ),
        migrations.AlterField(
            model_name='transporterdetails',
            name='transporter',
            field=models.ForeignKey(db_column='TransporterID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='vehicles', to='transit.transporter'),
        ),
    ]