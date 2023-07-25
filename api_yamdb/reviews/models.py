from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Класс Отзывов"""
    text=models.TextField(verbose_name='Текст')
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
    score=models.PositiveIntegerField(verbose_name='Оценка', validators=[
        MinValueValidator(
        1,message='Оценка ниже допустимой'), 
        MaxValueValidator(
        10,message='Оценка выше допустимой')]
        )
    
    pub_date=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title=models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews', verbose_name='Произведение')

    class Meta:
        verbose_name='отзыв'
        verbose_name_plural='отзывы'

    def __str__(self) -> str:
        return self.text
    

class Comment(models.Model):
    """Класс Комментариев"""
    text=models.TextField(verbose_name='Текст')
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    pub_date=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    review=models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', verbose_name='отзыв')

    class Meta:
        verbose_name='комментарий'
        verbose_name_plural='комментарии'

    def __str__(self) -> str:
        return self.text
    