
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator

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
        movies_list = Movie.objects.all()
        form = MovieFilterForm(request.GET)
        if form.is_valid():
            genre = form.cleaned_data.get('genre')
            if genre:
                movies_list = movies_list.filter(genres=genre)
            year = form.cleaned_data.get('year')
            if year:
                movies_list = movies_list.filter(release_year=year)
            rating = form.cleaned_data.get('rating')
            if rating:
                movies_list = movies_list.filter(original_rating__gte=rating)                
        paginator = Paginator(movies_list, 6)
        page_number = request.GET.get('page', 1)
        movies = paginator.page(page_number)
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
        movies = []
        form = MovieSearchForm(request.GET)
        query = None
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if query:
                movies = Movie.objects.annotate(
                    similarity=TrigramSimilarity('title', query),                    
                ).filter(similarity__gt=0.1).order_by('-similarity')
        return render(request, self.template_name, {'movies': movies,
                                                    'form': form,
                                                    'query': query})


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
