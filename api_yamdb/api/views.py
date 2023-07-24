from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from reviews.models import *


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Отзывы"""
    serializer_class=ReviewSerializer

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

    def get_review(self):
        review_id=self.kwargs.get('review_id')
        return get_object_or_404(Title, pk=review_id)    

    def get_queryset(self):
        return self.get_review().comments.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


