from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего!')
    if value < -3000:
        raise ValidationError('Год не может быть ранее 3000 до Н.Э.')
