# Generated by Django 4.1 on 2024-10-11 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_app', '0002_remove_rawmaterials_stock'),
        ('inventory_app', '0003_rawmaterials_stock_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawMaterialsStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now=True)),
                ('raw_materials', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='purchase_app.rawmaterials')),
            ],
        ),
        migrations.DeleteModel(
            name='RawMaterials_stock',
        ),
    ]
