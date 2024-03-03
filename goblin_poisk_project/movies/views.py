
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import UpdateView

from movies.models import Movie

from .forms import (DirectorForm, MovieFilterForm, MovieForm, MovieGenreForm,
                    MovieSearchForm)


class MovieListView(View):
    template_name = 'movies/movie_list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        movies = Movie.objects.all()
        form = MovieFilterForm(request.GET)
        if form.is_valid():
            genre = form.cleaned_data.get('genre')
            if genre:
                movies = movies.filter(genres=genre)
            year = form.cleaned_data.get('year')
            if year:
                movies = movies.filter(release_year=year)
            rating = form.cleaned_data.get('rating')
            if rating:
                movies = movies.filter(original_rating__gte=rating)
        return render(request, self.template_name, {'movies': movies, 'form': form})


class MovieDetailView(View):
    template_name = 'movies/movie_detail.html'

    def get(self, request: HttpRequest, movie_slug: str) -> HttpResponse:
        movie = get_object_or_404(Movie.objects.prefetch_related('genres').select_related('director'),
                                  slug=movie_slug)
        return render(request, self.template_name, {'movie': movie})


class MovieAdd(View):
    template_name = 'movies/movie_add.html'
    redirect_url = 'movies:movie_list'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = MovieForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(self.redirect_url))
        return render(request, self.template_name, {'form': form})


class MovieEdit(UpdateView):
    model = Movie
    template_name = 'movies/movie_edit.html'
    form_class = MovieForm
    success_url = 'movies:movie_detail'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'movie_slug': self.object.slug})

    def get_object(self, queryset=None):
        return get_object_or_404(Movie, slug=self.kwargs['movie_slug'])


class MovieSearch(View):
    template_name = 'movies/search.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        movies = Movie.objects.all()
        form = MovieSearchForm(request.GET)
        query = None
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if query:
                movies = movies.filter(title__icontains=query)
        return render(request, self.template_name, {'movies': movies, 'form': form, 'query': query})


class DirectorAdd(View):
    template_name = 'movies/director_add.html'
    redirect_template_name = 'movies/success_added_director_or_genre.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = DirectorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.redirect_template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class GenreAdd(View):
    template_name = 'movies/genre_add.html'
    redirect_template_name = 'movies/success_added_director_or_genre.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = MovieGenreForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = MovieGenreForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.redirect_template_name, {'form': form})
        return render(request, self.template_name, {'form': form})
