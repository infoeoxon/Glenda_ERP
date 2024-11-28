# Generated by Django 4.2 on 2024-11-28 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Damaged_good_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='water_Finished_goods_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='water_Finished_Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, unique=True)),
                ('size', models.CharField(max_length=150, null=True, unique=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('total_stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.water_finished_goods_category')),
            ],
        ),
        migrations.CreateModel(
            name='damaged_Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('total_stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production_app.damaged_good_category')),
            ],
        ),
    ]
