# Generated by Django 5.0 on 2024-01-28 09:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_customuser_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="organization",
        ),
    ]