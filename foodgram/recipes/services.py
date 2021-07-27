from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions

from foodgram.ingredients.models import Ingredient

from .models import Recipe, Tag


def add_recipe_with_ingredients_tags(serialized_data):
    """
    Creates new Recipe instance and adds tags & ingredients to it
    :param serialized_data: dict with cleaned data.
    :return: new Recipe object.
    """
    author = serialized_data.get('author')
    name = serialized_data.get('name')
    if Recipe.objects.filter(author=author, name=name).exists():
        raise exceptions.ValidationError(
            _('Вы уже публиковали рецепт с таким названием')
        )

    tags_data = serialized_data.pop('tags')
    ingredients_data = serialized_data.pop('ingredients')
    unique_ingredients = set()
    for ingredient in ingredients_data:
        if ingredient['id'] in unique_ingredients:
            raise exceptions.ValidationError(
                _('Ингредиенты в рецепте не должны повторяться')
            )
        unique_ingredients.add(ingredient['id'])
    new_recipe = Recipe.objects.create(**serialized_data)

    tags = []

    for tag in tags_data:
        tag_object = get_object_or_404(Tag, id=tag.id)
        tags.append(tag_object)
    new_recipe.tags.add(*tags)

    for ingredient in ingredients_data:
        ingredient_object = get_object_or_404(
            Ingredient, id=ingredient.get('id')
        )
        new_recipe.ingredients.add(
            ingredient_object,
            through_defaults={'amount': ingredient.get('amount')}
        )
    new_recipe.save()
    return new_recipe


def update_recipe_with_ingredients_tags(serialized_data, recipe_instance):
    """
    Edit recipe instance and add/remove tags/ingredients associated with it
    :param serialized_data: dict with cleaned data
    :param recipe_instance: Recipe object to update
    :return: updated Recipe object
    """
    tags_data = serialized_data.pop('tags')
    ingredients_data = serialized_data.pop('ingredients')
    unique_ingredients = set()

    for ingredient in ingredients_data:
        if ingredient.get('amount') <= 0:
            raise exceptions.ValidationError(
                _('Количество ингредиентов должно быть больше нуля')
            )
        if ingredient['id'] in unique_ingredients:
            raise exceptions.ValidationError(
                _('Ингредиенты в рецепте не должны повторяться')
            )
        unique_ingredients.add(ingredient['id'])

    recipe_instance.tags.clear()
    recipe_instance.ingredients.clear()
    recipe_instance.tags.add(*tags_data)

    for ingredient in ingredients_data:
        ingredient_object = get_object_or_404(
            Ingredient,
            id=ingredient.get('id')
        )
        recipe_instance.ingredients.add(
            ingredient_object,
            through_defaults={'amount': ingredient.get('amount')}
        )

    recipe_instance.name = serialized_data.get(
        'name', recipe_instance.name
    )
    recipe_instance.text = serialized_data.get(
        'text', recipe_instance.text
    )
    recipe_instance.cooking_time = serialized_data.get(
        'cooking_time', recipe_instance.cooking_time
    )
    recipe_instance.image = serialized_data.get(
        'image', recipe_instance.image
    )
    recipe_instance.save()
    return recipe_instance
