# Generated by Django 4.1.7 on 2024-09-22 04:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("soft_delete", "0004_foo_bar"),
    ]

    operations = [
        migrations.AddField(
            model_name="bar",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="foo",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]