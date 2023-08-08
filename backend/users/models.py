from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username_not_me

MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_FIRST_NAME = 150
MAX_LENGTH_LAST_NAME = 150
MAX_LENGTH_PASSWORD = 150


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_not_me,
        ],
    )
    first_name = models.CharField('Имя', max_length=MAX_LENGTH_FIRST_NAME)
    last_name = models.CharField('Фамилия', max_length=MAX_LENGTH_LAST_NAME)
    password = models.CharField('Пароль', max_length=MAX_LENGTH_PASSWORD)
