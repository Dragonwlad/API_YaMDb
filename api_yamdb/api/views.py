from django.shortcuts import render
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import TitleFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleSerealizer)
from .permissions import (IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly,
                          IsAdminOnly)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleSerealizer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')

    
class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Жанры"""
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Категории"""
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    # lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = ReviewSerializer

    def _get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def _get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def _get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        title = self._get_title()
        review = self._get_review()
        if review.title == title:
            serializer.save(author=self.request.user, review=review)

