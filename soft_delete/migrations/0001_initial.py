# Generated by Django 4.1.7 on 2024-09-13 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SoftDelete",
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
                ("deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
    ]