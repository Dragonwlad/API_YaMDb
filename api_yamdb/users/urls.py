
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import create_token, UsersViewSet, create_user, UserGetPath


v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet, basename='user')

urlpatterns = [
    path('users/me/', UserGetPath.as_view()),
    path('token/', create_token, name='token'),
    path('signup/', create_user, name='signup'),
    path('', include(v1_router.urls)),
]
