# Generated by Django 5.0.6 on 2024-11-29 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawMaterialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, unique=True)),
                ('size', models.CharField(max_length=150, null=True)),
                ('color', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('date', models.DateField(auto_now=True)),
                ('total_stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_app.rawmaterialcategory')),
            ],
        ),
        migrations.CreateModel(
            name='RFQ_raw_materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfq_number', models.CharField(max_length=50, null=True)),
                ('request_date', models.DateField(auto_now_add=True)),
                ('request_time', models.TimeField(auto_now_add=True)),
                ('requested_by', models.CharField(max_length=220, null=True)),
                ('approver', models.CharField(max_length=220, null=True)),
                ('quantity_needed', models.IntegerField()),
                ('batch_requirements', models.TextField(blank=True, null=True)),
                ('quality_standards', models.FileField(blank=True, null=True, upload_to='quality_standards/')),
                ('expected_delivery_date', models.DateField()),
                ('vendor_list', models.TextField(null=True)),
                ('preferred_vendors', models.TextField(null=True)),
                ('quotation_deadline', models.DateField()),
                ('delivery_address', models.TextField()),
                ('spoc_name', models.CharField(max_length=220, null=True)),
                ('spoc_number', models.BigIntegerField()),
                ('special_notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=220)),
                ('material_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rfq_raw_material_category', to='inventory_app.addcategory')),
                ('material_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rfq_raw_material_name', to='inventory_app.add_rawmaterial')),
            ],
        ),
    ]
