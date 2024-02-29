# Generated by Django 5.0.2 on 2024-02-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_order_is_cancelled_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('COD', 'Cash on Delivery')], default=True, max_length=10, null=True),
        ),
    ]
