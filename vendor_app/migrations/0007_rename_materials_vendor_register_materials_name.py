# Generated by Django 4.1.2 on 2024-11-29 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0006_alter_vendor_register_materials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor_register',
            old_name='materials',
            new_name='materials_name',
        ),
    ]
