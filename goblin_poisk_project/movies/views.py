from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import View

from movies.models import Movie


class MovieListView(View):
    template_name = 'movies/movie_list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        movies = get_list_or_404(Movie)
        return render(request, self.template_name, {'movies': movies})


class MovieDetailView(View):
    template_name = 'movies/movie_detail.html'

    def get(self, request: HttpRequest, movie_slug: str) -> HttpResponse:
        movie = get_object_or_404(Movie, slug=movie_slug)
        return render(request, self.template_name, {'movie': movie})
