# Generated by Django 5.0.6 on 2024-12-18 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="img",
            field=models.URLField(max_length=2000),
        ),
        migrations.AlterField(
            model_name="product",
            name="web",
            field=models.URLField(max_length=2000),
        ),
    ]
