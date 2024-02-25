from django.contrib.auth.models import User
from django.db import models
from transliterate import slugify


class MovieGenre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название жанра')
    description = models.CharField(max_length=300, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Director(models.Model):
    name = models.CharField(max_length=255, verbose_name='Режиссер')
    description = models.CharField(max_length=300, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'
        ordering = ['name']


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название фильма')
    release_year = models.PositiveSmallIntegerField(verbose_name='Год')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name='Режиссер')
    description = models.CharField(max_length=300, verbose_name='Описание')
    length = models.PositiveSmallIntegerField(verbose_name='Длительность')
    genres = models.ManyToManyField(MovieGenre, verbose_name='Жанры')
    original_rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Оригинальный рейтинг',
                                          null=True, blank=True)
    user_rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Рейтинг', null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name='Постер')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_year']),
        ]


class UserRating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Пользовательский рейтинг'
        verbose_name_plural = 'Пользовательские рейтинги'
        ordering = ['user']
        unique_together = ['user', 'movie']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    text = models.CharField(max_length=2000, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['created_at']
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.text
