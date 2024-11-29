# Generated by Django 4.1.3 on 2024-11-28 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer_registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_distributor', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('pincode', models.CharField(max_length=6, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('district', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('GST_yes_or_no', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=15, null=True)),
                ('GST_number', models.CharField(blank=True, max_length=15, null=True)),
                ('pan_yes_or_no', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=10, null=True)),
                ('PAN_number', models.CharField(blank=True, max_length=10, null=True)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
