# Generated by Django 5.0.2 on 2024-03-21 18:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MusicNotes",
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
                ("title", models.CharField(max_length=50)),
                ("duration", models.DurationField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                ("notes", models.FileField(blank=True, null=True, upload_to="pdf")),
                ("in_use", models.BooleanField(blank=True, null=True)),
                (
                    "date_posted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("voice", models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
