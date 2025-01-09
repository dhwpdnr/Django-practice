# Generated by Django 4.1.7 on 2025-01-09 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TableMetadata",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="FieldMetadata",
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
                ("name", models.CharField(max_length=255)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("CharField", "문자열 (CharField)"),
                            ("IntegerField", "정수 (IntegerField)"),
                            ("DecimalField", "소수 (DecimalField)"),
                            ("TextField", "텍스트 (TextField)"),
                        ],
                        max_length=50,
                    ),
                ),
                ("max_length", models.IntegerField(blank=True, null=True)),
                ("decimal_places", models.IntegerField(blank=True, null=True)),
                ("precision", models.IntegerField(blank=True, null=True)),
                ("is_required", models.BooleanField(default=False)),
                (
                    "default_value",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="fluid.tablemetadata",
                    ),
                ),
            ],
        ),
    ]
