# Generated by Django 4.1.2 on 2024-11-29 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0004_alter_vendor_register_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor_register',
            name='vendor_listofpdcts',
        ),
    ]
