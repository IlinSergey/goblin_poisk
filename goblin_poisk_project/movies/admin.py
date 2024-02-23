from django.contrib import admin
from movies.models import Director, Movie, MovieGenre, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'description', 'length', 'original_rating',)
    list_filter = ('title', 'genres', 'release_year',)
    search_fields = ('genres', 'title', 'release_year',)
    exclude = ('user_rating',)


@admin.register(MovieGenre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass