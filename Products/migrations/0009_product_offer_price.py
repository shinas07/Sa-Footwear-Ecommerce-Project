# Generated by Django 5.0.2 on 2024-03-10 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0008_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
