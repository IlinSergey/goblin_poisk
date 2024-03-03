# Generated by Django 4.2.3 on 2024-03-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0008_alter_director_name_alter_movie_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Название фильма"),
        ),
        migrations.AlterUniqueTogether(
            name="movie",
            unique_together={("title", "release_year", "director")},
        ),
    ]