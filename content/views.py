from django.shortcuts import render, get_object_or_404
from .models import Genre, Movie, Show, Season, Episode

#genre
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, 'genre_detail.html', {'genre': genre})

# Movies

def home(request):
    movies = Movie.objects.all()
    shows = Show.objects.all()
    genres = Genre.objects.all()
    return render(request, 'index.html', {'movies': movies, 'shows': shows, 'genres': genres})

def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    return render(request, 'movie_detail.html', {'movie': movie})


#Shows

def show_detail(request, slug):
    show = get_object_or_404(Show, slug=slug)
    seasons = Season.objects.filter(show=show)
    return render(request, 'show_detail.html', {'show': show, 'seasons': seasons})