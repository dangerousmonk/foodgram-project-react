from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_('email address')
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('last name'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username']

    def __str__(self):
        return self.get_full_name()


class UserSubscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscribers',
        on_delete=models.CASCADE
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('subscription date')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_subscription',
            )
        ]
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['-subscribed_at', 'id']

    def __str__(self):
        return f'{self.subscriber} - {self.subscription}'
