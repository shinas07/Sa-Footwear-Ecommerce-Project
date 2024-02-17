# Generated by Django 5.0.2 on 2024-02-16 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0001_initial'),
        ('Products', '0002_remove_product_brand_product_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Category.category'),
        ),
    ]
