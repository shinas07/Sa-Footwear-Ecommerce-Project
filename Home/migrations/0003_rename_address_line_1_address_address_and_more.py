# Generated by Django 5.0.2 on 2024-02-27 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_line_2',
        ),
    ]
