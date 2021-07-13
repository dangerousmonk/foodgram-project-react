from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import unique_slugify


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
        verbose_name=_('author'),
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
        'ingredients.Ingredient',
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
    created_date = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        verbose_name=_('created date'),
         )

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ['created_date']
        unique_together = ['author', 'name']

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredient_amounts',
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )
    ingredient = models.ForeignKey(
        'ingredients.Ingredient',
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
        #unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'


class Favourites(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='in_favourites',
        on_delete=models.CASCADE,
        verbose_name=_('recipe'),
    )
    added_at = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        verbose_name=_('added at')
    )

    class Meta:
        verbose_name = _('Favourites')
        verbose_name_plural = _('Favourites')
        ordering = ['-added_at', 'id']
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


