from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.db.models import Avg

from core.models import Category, Genre, Title, Review, Comment
from users.models import User
from .serializers import (CategorySerializer, GenreSerializer, TitleListSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleDetailSerializer, TitleManageSerealizer)
from .permissions import IsSuperUserIsAdminIsModeratorIsAuthor


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleManageSerealizer

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        if self.action == 'retrieve':
            return TitleDetailSerializer
        return super().get_serializer_class()


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Жанры"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Отзывы"""
    serializer_class=ReviewSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,
                         IsSuperUserIsAdminIsModeratorIsAuthor)
    # permission_classes=(permissions.AllowAny,)

    def save_actual_score(self):
        """Высчитывает и сохраняет рейтинг произведения"""
        title = self.get_title()
        avg_score = Title.objects.filter(id=title.id).aggregate(
            Avg('reviews__score')
            )
        title.rating = round(avg_score["reviews__score__avg"], 2)
        title.save()
    
    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset с отзывами для текущего произведения."""
        return self.get_title().reviews.all()
    
    def perform_create(self, serializer):
        """
        Создает отзыв для текущего произведения,
        где автором является текущий пользователь.
        """
        self.save_actual_score()
        author = User.objects.get(id=105)
        # serializer.save(author=author, title=self.get_title())
        serializer.save(author=self.request.user, title=self.get_title())

    def perform_update(self, serializer):
        self.save_actual_score()
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для объектов модели Comment.
    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Возвращает queryset с комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """
        Создает комментарий для текущего отзыва,
        где автором является текущий пользователь.
        """
        serializer.save(author=self.request.user, review=self.get_review())