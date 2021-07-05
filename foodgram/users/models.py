from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('Email адрес'),
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        blank=False,
        null=False,
    )
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'