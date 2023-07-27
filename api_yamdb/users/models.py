from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):
    '''Класс пользователей.'''
    username_regex = '^[\w.@+-]+\z'
    # Валидация данных
    username_validator = RegexValidator(
        regex=username_regex,
        message='Username может содержать только буквы, цифры и @/./+/-/_',
        code='invalid_username'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    confirmation_code = models.CharField(max_length=5, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default='user'
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
