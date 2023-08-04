from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Класс пользователей."""
    class Role(models.TextChoices):
        """Роли пользователей."""
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Администратор'
        USER = 'user', 'Администратор'

    # Валидация данных
    username_regex = r'[\w.@+-]+$'
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
        choices=Role.choices,
        default=Role.USER
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        unique_together = ('username', 'email')

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_user(self):
        return self.role == self.Role.USER

    def __str__(self):
        return self.username
