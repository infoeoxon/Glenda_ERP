# Generated by Django 4.2.12 on 2024-12-02 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0003_alter_employeedetails_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='check_in_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='check_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
