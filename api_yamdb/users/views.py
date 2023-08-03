import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminOnly
from users.serializers import (
    AdminCreateUserSerializer, UserCreateSerializer, UserPathSerializer)
from users.models import User


def get_confirmation_code():
    return secrets.token_urlsafe(3)


def send_confirmation_code(user_email, confirmation_code):
    send_mail(
        subject='confirmation_code',
        message=f'confirmation_code - {confirmation_code}',
        from_email='from@example.com',
        recipient_list=[user_email],
        fail_silently=True,
    )


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_user(request):

    serializer = UserCreateSerializer(data=request.data)

    if serializer.is_valid():
        user_email = request.data['email']
        confirmation_code = get_confirmation_code()
        serializer.save(
            confirmation_code=confirmation_code
        )
        send_confirmation_code(user_email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif ('unique' in str(serializer.errors.get('email'))
          and 'unique' in str(serializer.errors.get('username'))):
        user = User.objects.get(username=request.data['username'])
        send_confirmation_code(
            user_email=user.email,
            confirmation_code=user.confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
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
        confirmation_code = get_confirmation_code()
        serializer.save(confirmation_code=confirmation_code)


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
