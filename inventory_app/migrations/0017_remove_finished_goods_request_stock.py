# Generated by Django 5.0.6 on 2024-10-23 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0016_alter_finished_goods_request_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finished_goods_request',
            name='stock',
        ),
    ]
