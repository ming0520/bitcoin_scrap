# Generated by Django 5.0.2 on 2024-02-26 06:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scrap", "0006_bitstampdataminute"),
    ]

    operations = [
        migrations.AddField(
            model_name="commentraw",
            name="status",
            field=models.CharField(default="PENDING", max_length=10),
        ),
        migrations.AddField(
            model_name="postraw",
            name="status",
            field=models.CharField(default="PENDING", max_length=10),
        ),
    ]
