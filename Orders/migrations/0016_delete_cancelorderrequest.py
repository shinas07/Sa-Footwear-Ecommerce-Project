# Generated by Django 5.0.2 on 2024-03-13 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0015_cancelorderrequest'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CancelOrderRequest',
        ),
    ]