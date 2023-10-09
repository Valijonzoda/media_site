from django.contrib import admin
from django.forms import TextInput

from . import models
from .models import (
    Genre,
    Movie,
    Season,
    Show,
    Episode,
    Source,
    EpisodeSource,
    MovieSource,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class MovieSourceInline(admin.StackedInline):
    model = MovieSource
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("genres",)
    # search fields
    search_fields = ["name"]
    inlines = [MovieSourceInline]
    fields = (
        "name",
        "description",
        "release_year",
        "genres",
        "image",
        "kinopoisk_rating",
        "imdb_rating",
        "kinopoisk_code",
        "imdb_code",
    )


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "description",
        "first_aired",
        "genres",
        "image",
        "slug",
        "kinopoisk_rating",
        "imdb_rating",
        "kinopoisk_code",
        "imdb_code",
    )
    pass


class EpisodeSourceInline(admin.StackedInline):
    model = EpisodeSource
    extra = 1


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    inlines = [EpisodeSourceInline]
