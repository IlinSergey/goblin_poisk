from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path("", views.MovieListView.as_view(), name="movie_list"),
    path("<slug:movie_slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("director/add/", views.DirectorAdd.as_view(), name="director_add"),
    path("genre/add/", views.GenreAdd.as_view(), name="genre_add"),
    path("movie/add/", views.MovieAdd.as_view(), name="movie_add"),
    path("<slug:movie_slug>/edit/", views.MovieEdit.as_view(), name="movie_edit"),
]
