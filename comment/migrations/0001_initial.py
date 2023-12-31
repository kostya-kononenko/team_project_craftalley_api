# Generated by Django 4.2.6 on 2023-10-17 11:08

import comment.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=comment.models.comment_image_file_path,
                    ),
                ),
                ("date_posted", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
