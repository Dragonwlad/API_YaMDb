from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):
    '''Класс пользователей.'''
<<<<<<< HEAD
    username_regex = '^[\w.@+-]+\z'
=======
    username_regex = r'[\w.@+-]+\z'
>>>>>>> 9474fa5 (настроил users победил ошибки)
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

<<<<<<< HEAD
    confirmation_code = models.CharField(max_length=5)
=======
    confirmation_code = models.CharField(max_length=5, blank=True)
>>>>>>> 9474fa5 (настроил users победил ошибки)
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

    class Meta:
        unique_together = ('username', 'email')

    @property
    def is_admin(self):
        return self.role == ROLE_CHOICES[0][0] or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == ROLE_CHOICES[1][1]

    @property
    def is_user(self):
        return self.role == ROLE_CHOICES[2][2]

    def __str__(self):
        return self.username
