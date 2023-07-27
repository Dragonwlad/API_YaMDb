from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):

    username_regex = '^[\w.@+-]+\z'
    username_validator = RegexValidator(
        regex=username_regex,
        message='Username может содержать только буквы, цифры и @/./+/-/_',
        code='invalid_username'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    password = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254)
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
