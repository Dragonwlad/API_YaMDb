import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import AdminCreateUserSerializer, UserCreateSerializer
from users.models import User


def create_and_send_confirmation_code(user_email):
    confirmation_code = secrets.token_urlsafe(4)
    send_mail(
        subject='confirmation_code',
        message=f'confirmation_code - {confirmation_code}',
        from_email='from@example.com',
        recipient_list=[user_email],
        fail_silently=True,
    )
    return confirmation_code


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_user(request):

    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user_email = request.data['email']
        serializer.save(
            confirmation_code=create_and_send_confirmation_code(user_email)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        print('------------', (serializer.errors.get('email')['code']))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
{'username': [ErrorDetail(string='пользователь с таким username уже существует.', code='unique')],
 'email': [ErrorDetail(string='пользователь с таким email уже существует.', code='unique')]
 }
{'email': [ErrorDetail(string='Введите правильный адрес электронной почты.', code='invalid')]}
'''


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    permission_classes = (AllowAny, )  # после отладки установить ->(IsAdminUser, )
    lookup_field = 'username'

    def perform_create(self, serializer):
        user_email = serializer.validated_data['email']
        serializer.save(
            confirmation_code=create_and_send_confirmation_code(user_email)
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


class UserGetPath(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

