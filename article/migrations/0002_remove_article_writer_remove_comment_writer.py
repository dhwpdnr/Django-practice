# Generated by Django 4.1.7 on 2024-02-20 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="writer",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="writer",
        ),
    ]
