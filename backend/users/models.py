from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username_not_me


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=settings.MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_not_me,
        ],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LENGTH_FIRST_NAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LENGTH_LAST_NAME,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.MAX_LENGTH_PASSWORD,
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    """Модель подписок на пользователей."""

    follower = models.ForeignKey(
        User,
        verbose_name='подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='подписан на',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_follow',
                fields=['follower', 'following'],
            ),
            models.CheckConstraint(
                name='cant_subscribe_to_self',
                check=~models.Q(follower=models.F('following')),
                violation_error_message='Нельзя подписаться на самого себя',
            ),
        ]

    def __str__(self):
        return f'{self.follower.username} -> {self.following.username}'
