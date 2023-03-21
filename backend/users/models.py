from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """ Модель пользователя. """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    username = models.CharField(
        verbose_name='Логин', max_length=150, unique=True,
        blank=False, validators=(UnicodeUsernameValidator, ),
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150,
    )
    email = models.EmailField(
        verbose_name='Email', max_length=254, unique=True,
    )
    is_subscribed = models.BooleanField(
        verbose_name='Подписан ли текущий пользователь на этого',
        default=False,
    )
    password = models.CharField(
        verbose_name='Пароль', max_length=150,
    )

    class Meta:
        unique_together = ('email',)
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe')
        ]

    def __str__(self):
        return f'{self.user} id - {self.user.pk}, {self.author}'
