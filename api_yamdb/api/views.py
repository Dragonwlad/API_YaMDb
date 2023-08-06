from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleSerializer, AdminCreateUserSerializer,
                          UserCreateSerializer, UserPathSerializer,
                          TitleCreateSerializer)
from .permissions import IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly
from .filters import TitleFilter
from .permissions import IsAdminOnly
from django.conf import settings


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Для объектов модели Произведения"""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return super().get_serializer_class()


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


def get_confirmation_code(user):
    return default_token_generator.make_token(user)


def send_confirmation_code(user_email, confirmation_code):
    send_mail(
        subject='Подтвердите ваш email адрес для завершения регистрации',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[user_email],
        fail_silently=True,
    )


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_user(request):
    """Самостоятельная регистрация пользователя."""
    serializer = UserCreateSerializer(data=request.data)
    user_email = request.data.get('email')
    username = request.data.get('username')

    if User.objects.filter(username=username, email=user_email):
        user = User.objects.get(username=request.data['username'])
        send_confirmation_code(
            user_email=user.email,
            confirmation_code=user.confirmation_code
        )
        return Response(
            {'message': 'Пользователь с данным email уже существует. '
             'Код подтверждения повторно отправлен.'
             },
            status=status.HTTP_200_OK
        )

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=username)
    confirmation_code = get_confirmation_code(user)
    serializer.save(
        confirmation_code=confirmation_code
    )
    send_confirmation_code(user_email, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet для просмотра пользователей и редактирования
    данных пользователя."""
    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOnly, )
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=self.request.data.get('username'))
        confirmation_code = get_confirmation_code(user)
        serializer.save(
            confirmation_code=confirmation_code
        )


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_token(request):
    username = request.data.get('username', None)
    confirmation_code = request.data.get('confirmation_code', None)
    if not username:
        return Response(
            {'username': 'Обязательное поле.'},
            status=status.HTTP_400_BAD_REQUEST)
    if not confirmation_code:
        return Response(
            {'confirmation_code': 'Обязательное поле.'},
            status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    correct_confirmation_code = user.confirmation_code
    if confirmation_code == correct_confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_201_CREATED)
    else:
        return Response('Неверный confirmation_code',
                        status=status.HTTP_400_BAD_REQUEST)


class UserGetPath(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = AdminCreateUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserPathSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.get(request)
