# Generated by Django 5.0.3 on 2024-03-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_remove_location_name_alter_shipment_total_est"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="address",
            field=models.CharField(max_length=255),
        ),
    ]
