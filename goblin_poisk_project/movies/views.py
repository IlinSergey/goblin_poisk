from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from movies.models import Movie


class MovieListView(View):
    template_name = 'movies/movie_list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        movies = Movie.objects.all()
        return render(request, self.template_name, {'movies': movies})
