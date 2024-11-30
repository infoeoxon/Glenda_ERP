# Generated by Django 5.0.6 on 2024-11-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_app', '0002_alter_rfq_raw_materials_vendor_list'),
        ('vendor_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfq_raw_materials',
            name='vendor_list',
        ),
        migrations.AddField(
            model_name='rfq_raw_materials',
            name='vendor_list',
            field=models.ManyToManyField(related_name='vendor_list_rfq', to='vendor_app.vendor_register'),
        ),
    ]