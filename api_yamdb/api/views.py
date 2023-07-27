from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from core.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleListSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleDetailSerializer, TitleManageSerealizer)
from .permissions import IsSuperUserIsAdminIsModeratorIsAuthor


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleManageSerealizer

    def get_serializer_class(self):
        # print(f'>>>>>>>>{self.action}')
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
    """Вьюсет Для объектов модели Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Отзывы"""
    serializer_class=ReviewSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,
                         IsSuperUserIsAdminIsModeratorIsAuthor)

    def get_title(self):
        title_id=self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)    

    def get_queryset(self):
        return self.get_title().reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):    
    """Вьюсет Для объектов модели Комментарии"""
    serializer_class=CommentSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,
                         IsSuperUserIsAdminIsModeratorIsAuthor)

    permission_classes=(permissions.IsAuthenticatedOrReadOnly,
                         IsSuperUserIsAdminIsModeratorIsAuthor)


    def get_review(self):
        review_id=self.kwargs.get('review_id')
        return get_object_or_404(Title, pk=review_id)    

    def get_queryset(self):
        return self.get_review().comments.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

