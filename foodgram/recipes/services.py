from .models import Recipe, Tag
from foodgram.ingredients.models import Ingredient


def add_recipe_with_ingredients_tags(serialized_data):
    """
    Creates new Recipe instance and adds tags & ingredients to it
    :param serialized_data: dict with cleaned data.
    :return: new Recipe object.
    """
    tags_data = serialized_data.pop('tags')
    ingredients_data = serialized_data.pop('ingredients')
    new_recipe = Recipe.objects.create(**serialized_data)
    tags = []
    for tag in tags_data:
        tag_object = Tag.objects.get(id=tag.id)
        tags.append(tag_object)
    new_recipe.tags.add(*tags)
    for ingredient in ingredients_data:
        ingredient_object = Ingredient.objects.get(id=ingredient['id'])
        new_recipe.ingredients.add(ingredient_object, through_defaults={'amount': ingredient['amount']})
    new_recipe.save()
    return new_recipe


def update_recipe_with_ingredients_tags(serialized_data, recipe_instance):
    """
    Edit recipe instance and add/remove tags/ingredients associated with it
    :param serialized_data: dict with cleaned data
    :param recipe_instance: Recipe object to update
    :return: updated Recipe object
    """
    from collections import OrderedDict, defaultdict
    tags_data = serialized_data.pop('tags')
    ingredients_data = serialized_data.pop('ingredients')
    recipe_instance.tags.clear()
    recipe_instance.ingredients.clear()
    recipe_instance.tags.add(*tags_data)
    for ingredient in ingredients_data:
        ingredient_object = Ingredient.objects.get(id=ingredient['id'])
        recipe_instance.ingredients.add(ingredient_object, through_defaults={'amount': ingredient.get('amount')})
    recipe_instance.name = serialized_data.get('name', recipe_instance.name)
    recipe_instance.text = serialized_data.get('text', recipe_instance.text)
    recipe_instance.cooking_time = serialized_data.get('cooking_time', recipe_instance.cooking_time)
    recipe_instance.image = serialized_data.get('image', recipe_instance.image)
    recipe_instance.save()
    return recipe_instance
