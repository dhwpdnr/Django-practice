# Generated by Django 4.1.7 on 2025-02-05 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
