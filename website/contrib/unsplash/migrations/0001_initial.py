# Generated by Django 4.0.6 on 2022-09-04 14:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []  # type: ignore

    operations = [
        migrations.CreateModel(
            name="UnsplashPhoto",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unsplash_id",
                    models.CharField(db_index=True, max_length=11, unique=True),
                ),
                ("data", models.JSONField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "data_last_updated",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]
