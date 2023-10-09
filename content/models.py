from datetime import datetime

import abstract
import django
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ManyToManyField
from django.template.defaultfilters import slugify


# Genre models
class Genre(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="genre_images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    VIDEO_QUALITY_CHOICES = [
        ("HD", "480p"),
        ("Full_HD", "1080p"),
        ("4K", "2160p"),
    ]
    video_quality = models.CharField(max_length=10, choices=VIDEO_QUALITY_CHOICES)
    url = models.URLField(
        max_length=200,
    )
    created_at = models.DateField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Show(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    first_aired = models.DateField()
    genres = models.ManyToManyField(Genre, related_name="genre")
    image = models.ImageField(upload_to="show_images", blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    kinopoisk_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10)],
        blank=False,
    )
    imdb_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10)],
        blank=False,
    )
    kinopoisk_code = models.CharField(max_length=25, null=True, blank=True)
    imdb_code = models.CharField(max_length=25, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Show, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Season(models.Model):
    season_number = models.PositiveIntegerField()
    descriptions = models.TextField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shows/seasons/", blank=True, null=True)

    def __str__(self):
        return f"Season {self.season_number} of {self.show}"


class MovieSource(Source):
    movie = models.ForeignKey(
        "Movie", on_delete=models.CASCADE, related_name="movie_sources"
    )

    def __str__(self):
        return f"{self.url}"


class EpisodeSource(Source):
    episode = models.ForeignKey(
        "Episode", on_delete=models.CASCADE, related_name="episode_sources"
    )

    def __str__(self):
        return f"{self.url}"


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.CharField(max_length=5)
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to="movie_images/", blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    kinopoisk_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10)],
        blank=False,
    )
    imdb_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10)],
        blank=False,
    )
    kinopoisk_code = models.CharField(max_length=25, null=True, blank=True)
    imdb_code = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name


class Episode(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=100)
    episode_number = models.PositiveIntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="season")
    image = models.ImageField(upload_to="shows/seasons/episode", blank=True, null=True)

    def __str__(self):
        return f"Episode {self.episode_number} of {self.season}"
