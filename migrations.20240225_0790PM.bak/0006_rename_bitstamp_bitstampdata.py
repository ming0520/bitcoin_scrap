# Generated by Django 5.0.2 on 2024-02-25 10:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scrap", "0005_alter_bitstamp_close_alter_bitstamp_high_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Bitstamp",
            new_name="BitstampData",
        ),
    ]
