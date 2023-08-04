from rest_framework import viewsets, mixins
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Title, Review
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleSerializer)
from .permissions import IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly
from api.filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Произведения"""
    # queryset = Title.objects.all()
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    # queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryGenreMixin(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreMixin):
    """Вьюсет Для объектов модели Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """Вьюсет Для объектов модели Жанры"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = ReviewSerializer

    def _get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def _get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def _get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        title = self._get_title()
        review = self._get_review()
        if review.title == title:
            serializer.save(author=self.request.user, review=review)
