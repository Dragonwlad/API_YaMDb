from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import mixins

from api.permissions import IsAdminOnly
from users.serializers import (
    AdminCreateUserSerializer, UserCreateSerializer, UserPathSerializer)
from users.models import User
from api_yamdb.settings import SERVER_EMAIL


def get_confirmation_code(user):
    return default_token_generator.make_token(user)


def send_confirmation_code(user_email, confirmation_code):
    send_mail(
        subject='Подтвердите ваш email адрес для завершения регистрации',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=SERVER_EMAIL,
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
