# Generated by Django 5.0.6 on 2024-12-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_product_shop_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailCode",
            fields=[
                ("email_code_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254)),
                ("code", models.CharField(max_length=20)),
                ("datetime", models.DateTimeField()),
            ],
        ),
    ]
