from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response

from core.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleListSerializer,ReviewSerializer,
                          CommentSerializer,TitleDetailSerializer,
                          TitleManageSerealizer)
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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        reviews = Review.objects.filter(title=instance)
        score_sum = 0
        if reviews.count() != 0:
            for review in reviews:
                score_sum += review.score
                print(f'{reviews.count()}>>>>>>>>>>>>{score_sum}')
            instance.rating = round(score_sum / reviews.count(), 2)
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

