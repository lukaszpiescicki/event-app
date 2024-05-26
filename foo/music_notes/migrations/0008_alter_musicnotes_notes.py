# Generated by Django 5.0.2 on 2024-05-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music_notes", "0007_alter_musicnotes_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musicnotes",
            name="notes",
            field=models.FileField(
                blank=True,
                help_text="Pdf file of music notes",
                null=True,
                upload_to="pdf",
            ),
        ),
    ]