# Generated by Django 5.0.2 on 2024-03-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_cancelorder_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
