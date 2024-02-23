from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path("", views.MovieListView.as_view(), name="movie_list"),
    path("<int:movie_id>/", views.MovieDetailView.as_view(), name="movie_detail"),
]
