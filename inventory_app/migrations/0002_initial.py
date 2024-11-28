# Generated by Django 4.2 on 2024-11-28 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory_app', '0001_initial'),
        ('purchase_app', '0001_initial'),
        ('production_app', '0001_initial'),
        ('register_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='raw_material_request',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='register_app.department'),
        ),
        migrations.AddField(
            model_name='raw_material_request',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_app.rawmaterials'),
        ),
        migrations.AddField(
            model_name='raw_material_allocate',
            name='raw_material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_app.rawmaterials'),
        ),
        migrations.AddField(
            model_name='finished_goods_stock',
            name='finished_goods',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='production_app.water_finished_goods'),
        ),
        migrations.AddField(
            model_name='finished_goods_request',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.water_finished_goods_category'),
        ),
        migrations.AddField(
            model_name='finished_goods_request',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register_app.department'),
        ),
        migrations.AddField(
            model_name='finished_goods_request',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.water_finished_goods'),
        ),
        migrations.AddField(
            model_name='finished_goods_allocate',
            name='finished_good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.water_finished_goods'),
        ),
        migrations.AddField(
            model_name='damaged_goods_stock',
            name='damaged',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='production_app.damaged_goods'),
        ),
    ]
