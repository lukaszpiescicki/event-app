# Generated by Django 5.0.2 on 2024-03-21 18:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_initial"),
        ("music_notes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="repertoire",
            field=models.ManyToManyField(
                blank=True, null=True, to="music_notes.musicnotes"
            ),
        ),
    ]
