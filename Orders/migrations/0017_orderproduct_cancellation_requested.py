# Generated by Django 5.0.2 on 2024-03-13 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0016_delete_cancelorderrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='cancellation_requested',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
