# Generated by Django 5.0.6 on 2024-10-23 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0015_alter_finished_goods_request_department'),
        ('register_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finished_goods_request',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register_app.department'),
        ),
    ]
