# Generated by Django 5.0.2 on 2024-03-13 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0018_cancellationrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='cancellation_requested',
        ),
        migrations.DeleteModel(
            name='CancellationRequest',
        ),
    ]
