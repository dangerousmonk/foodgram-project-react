from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class MeasurementUnit(models.Model):
    class Metrics(models.TextChoices):
        mass = _('mass'), _('mass')
        volume = _('volume'), _('volume')
        quantity = _('quantity'), _('quantity')
        percent = _('percent'), _('percent')
        miscellaneous = _('miscellaneous'), _('miscellaneous')

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_('name'),
    )
    metric = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=Metrics.choices,
        verbose_name=_('metric'),
    )

    class Meta:
        verbose_name = _('Measurement unit')
        verbose_name_plural = _('Measurement units')
        ordering = ['metric', 'name']
        unique_together = ['name', 'metric']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('name'),
        db_index=True,
    )
    measurement_unit = models.ForeignKey(
        'MeasurementUnit',
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name=_('measurement unit'),
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ['measurement_unit', 'name']
        unique_together = ['name', 'measurement_unit']

    def __str__(self):
        return self.name
