
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import create_token, UsersViewSet, create_user


v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/token/', create_token, name='token'),
    path('v1/auth/signup/', create_user, name='signup'),
    # path('v1/auth/signup/', create_user, name='signup'),
]
