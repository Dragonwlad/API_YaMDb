from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from .validators import year_validator


class Category(models.Model):
    """Модель данных для категорий."""
    name = models.CharField('Название',
                            max_length=256)
    slug = models.SlugField('Slug',
                            max_length=50,
                            unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель данных для жанров."""
    name = models.CharField('Название',
                            max_length=256)
    slug = models.SlugField('Slug',
                            max_length=50,
                            unique=True
                            )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title (models.Model):
    """Модель данных для произведений."""
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год',
                               validators=[year_validator, ]
                               )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   through='TitleGenre'
                                   )
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель данных для отзывов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст")
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name="Оценка"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="only_one_review_allowed"
            ),
        ]

        def __str__(self):
            return self.text[:settings.STRING_OUTPUT_LENGTH]


class Comment(models.Model):
    """Модель данных для комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Комментарий")
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:settings.STRING_OUTPUT_LENGTH]
