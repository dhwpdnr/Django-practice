# Generated by Django 4.1.7 on 2024-09-22 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("soft_delete", "0003_alter_softdelete_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Foo",
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
        migrations.CreateModel(
            name="Bar",
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
                (
                    "foo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="soft_delete.foo",
                    ),
                ),
            ],
        ),
    ]