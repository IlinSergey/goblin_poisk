from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import View

from .forms import DirectorForm
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


class DirectorAdd(View):
    template_name = 'movies/director_add.html'
    redirect_template_name = 'movies/movie_list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = DirectorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.redirect_template_name, {'form': form})
        return render(request, self.template_name, {'form': form})
