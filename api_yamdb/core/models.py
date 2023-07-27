from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Genre(models.Model):
    name = models.CharField('Название',
                            max_length=20)
    slug = models.SlugField('Slug',
                            max_length=20,
                            unique=True
                            )
    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'



class Category(models.Model):
    name = models.CharField('Название',
                            max_length=20)
    slug = models.SlugField('Slug',
                            max_length=20,
                            unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title (models.Model):

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', blank=True)
    rating = models.DecimalField(blank=True,
                                 null=True,
                                 max_digits=3, decimal_places=1)
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
    """Класс Отзывов"""
    text=models.TextField(verbose_name='Текст')
    author=models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews',
                             verbose_name='Автор')
    score=models.PositiveIntegerField(verbose_name='Оценка', validators=[
        MinValueValidator(
        1,message='Оценка ниже допустимой'), 
        MaxValueValidator(
        10,message='Оценка выше допустимой')]
        )
    
    pub_date=models.DateTimeField(auto_now_add=True,
                                  verbose_name='Дата публикации')
    title=models.ForeignKey(Title,
                            on_delete=models.CASCADE,
                            related_name='reviews',
                            verbose_name='Произведение')

    class Meta:
        verbose_name='отзыв'
        verbose_name_plural='отзывы'

    def __str__(self) -> str:
        return self.text
    

class Comment(models.Model):
    """Класс Комментариев"""
    text=models.TextField(verbose_name='Текст')
    author=models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Автор')
    pub_date=models.DateTimeField(auto_now_add=True,
                                  verbose_name='Дата публикации')
    review=models.ForeignKey(Review,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='отзыв')

    class Meta:
        verbose_name='комментарий'
        verbose_name_plural='комментарии'

    def __str__(self) -> str:
        return self.text
    