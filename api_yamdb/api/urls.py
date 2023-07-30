from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                    ReviewViewSet, CommentViewSet)

from rest_framework.routers import DefaultRouter

from users.views import create_token, UsersViewSet, create_user, UserGetPath


v1_router = DefaultRouter()

v1_router.register('', UsersViewSet)
router = SimpleRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserGetPath.as_view()),
    path('v1/token/', create_token, name='token'),
    path('v1/signup/', create_user, name='signup'),
    path('v1/users/', include(v1_router.urls)),
    path('v1/', include(router.urls)),
]
