# Generated by Django 4.2.3 on 2024-02-22 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_alter_moviegenre_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Director",
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
                ("name", models.CharField(max_length=255, verbose_name="Режиссера")),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=300, null=True, verbose_name="Описание"
                    ),
                ),
            ],
            options={
                "verbose_name": "Режиссер",
                "verbose_name_plural": "Режиссеры",
                "ordering": ["name"],
            },
        ),
        migrations.AlterField(
            model_name="movie",
            name="director",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.director",
                verbose_name="Режиссер",
            ),
        ),
    ]
