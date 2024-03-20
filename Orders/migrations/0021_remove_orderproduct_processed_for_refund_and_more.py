# Generated by Django 5.0.2 on 2024-03-18 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_address_name'),
        ('Orders', '0020_orderproduct_processed_for_refund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='processed_for_refund',
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.address'),
        ),
    ]