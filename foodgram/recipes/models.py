from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import unique_slugify


class MeasurementUnit(models.Model):
    class Metrics(models.TextChoices):
        mass = _('mass'), _('mass')
        volume = _('volume'), _('volume')
        quantity = _('quantity'), _('quantity')

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
        verbose_name=_('name'),
    )
    measurement_unit = models.ForeignKey(
        'MeasurementUnit',
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name=_('ingredients'),
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ['measurement_unit', 'name']
        unique_together = ['name', 'measurement_unit']

    def __str__(self):
        return self.name


class Tag(models.Model):
    # TODO: unique name
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_('name'),
    )
    # TODO: unique color?
    color = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        default='#E26C2D',
        verbose_name=_('color'),
    )
    slug = models.SlugField(
        max_length=255,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_('slug'),
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slugify(self.name, self.__class__)
        return super().save(*args, **kwargs)


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('recipe author')
        # TODO : keep recipes
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_('name'),
    )
    # TODO: make less chaotic upload
    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('select image to upload'),
        null=False,
        blank=False,
        upload_to='recipes/',
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('description'),
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name=_('tags'),
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        through='IngredientAmount',
        verbose_name=_('ingredients'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
        verbose_name=_('cooking time'),
    )


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredient_amounts',
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        related_name='ingredient_amounts',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('ingredient')
    )
    amount = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
        verbose_name=_('ingredient amount')
    )

    class Meta:
        verbose_name = _('Ingredient amount')
        verbose_name_plural = _('Ingredient amounts')
        ordering = ['id']
