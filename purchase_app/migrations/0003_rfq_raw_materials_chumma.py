# Generated by Django 4.1 on 2024-11-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("purchase_app", "0002_rfq_raw_materials"),
    ]

    operations = [
        migrations.AddField(
            model_name="rfq_raw_materials",
            name="chumma",
            field=models.TextField(null=True),
        ),
    ]
