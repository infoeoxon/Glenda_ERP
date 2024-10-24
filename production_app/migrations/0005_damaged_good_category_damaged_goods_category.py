# Generated by Django 4.1 on 2024-10-18 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production_app', '0004_water_finished_goods_total_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Damaged_good_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='damaged_goods',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.damaged_good_category'),
        ),
    ]
