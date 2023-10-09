import requests
from media_site.celery_app import *
from .models import Show, Movie, MovieSource
from requests.exceptions import ConnectionError
from decouple import config

MY_KP_API = config('MY_KP_API')

@app.task
def get_shows():
    url = 'https://channelsapi.s3.amazonaws.com/media/test/shows.json'
    response = requests.head(url)
    shows_data = response.json()

    for show_data in shows_data:
        slug = show_data['slug']
        imdb_rating = show_data['imdb_rating']

        show = Show.objects.filter(slug=slug).first()
        if show is None:
            show=Movie(slug=slug)
        show.name = show_data.get("name")
        show.imdb_rating = show_data.get("imdb_rating")
        show.image = show_data['image']
        show.description = show_data['description']
        show_data.first_aired=show_data.get('first_aired')
        show.imdb_rating = imdb_rating
        show.save()

@app.task
def get_movies():
    url = 'https://channelsapi.s3.amazonaws.com/media/test/movies.json'
    response = requests.head(url)
    movies_data = response.json()

    for movie_data in movies_data:
        slug = movie_data['slug']
        imdb_rating = movie_data['imdb_rating']

        movie = Movie.objects.filter(slug=slug).first()
        if movie is None:
            movie = Movie(slug=slug)
        movie.name = movie_data.get("name")
        movie.imdb_rating = movie_data.get("imdb_rating")
        movie.image = movie_data['image']
        movie.description = movie_data['description']
        movie.release_year = movie_data.get('release_year')
        movie.imdb_rating = imdb_rating
        movie.save()



#get kinopoisk rating using kinopoisk_api

@app.task
def get_movie_kinopisk_rating():
    movies = Movie.objects.filter(kinopoisk_code__isnull=False)
    for movie in movies:
        url = f'https://api.kinopoisk.dev/v1.3/movie/{movie.kinopoisk_code}'
        headers = {
            'accept': 'application/json',
            'X-API-KEY': MY_KP_API
        }

        response = requests.get(url,headers=headers)
        if response.ok:
            kp_data = response.json()
            for doc in kp_data.get('docs', []):
                movie_rating = doc.get("rating")
                print(movie_rating)
                movie = Movie.objects.filter(kinopoisk_code=movie_rating).first()
                if movie is None:
                    print("movie not found(")
                else:
                    movie.kinopoisk_code = movie_rating
                    movie.save()
                    print("rating update")
        else:
            print("some server error")


@app.task
def get_kinopoisk_id_by_name():
    movie_names = Movie.objects.values_list('name', flat=True)
    for movie in movie_names:
        print(movie)
        url = f'https://api.kinopoisk.dev/v1.2/movie/search?page=1&limit=1&query={movie}'
        headers = {
            'accept': 'application/json',
            'X-API-KEY': MY_KP_API
        }
        response = requests.get(url, headers=headers)
        kp_movie_data = response.json()
        for doc in kp_movie_data.get('docs', []):
            movie_id = doc.get('id')
            alternative_name = doc.get('alternativeName')
            movie = Movie.objects.filter(name=alternative_name).first()
            if movie is None:
                print("movie not found")
            else:
                movie.kinopoisk_code = movie_id
                movie.save()
                print("movie id update")




@app.task
def check_source_test():
    for movie_name in Movie.objects.values_list('name', flat=True):
        try:
            movie = Movie.objects.get(name=movie_name)
            movie_sources = MovieSource.objects.filter(movie=movie)

            for source in movie_sources:
                url = source.url
                try:
                    response = requests.head(url)
                    source.is_valid = response.ok
                except ConnectionError:
                    source.is_valid = False
                source.save()
        except:
            print(f'Movie same error')
