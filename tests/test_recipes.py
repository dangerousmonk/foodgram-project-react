import os
import random
import shutil

from django.urls import reverse

import pytest
from rest_framework.test import override_settings

from foodgram.recipes.models import FavouriteRecipe, Recipe

from . import factories
from .config import BASE_DIR

TEMP_DIR = 'test_files'


class TestRecipes:
    # status flags -> is_in_shopping_cart & is_favorited
    LIST_ENDPOINT = reverse('recipes-list')
    RECIPES_NUM = 8
    INGREDIENTS_NUM = 4
    PAGE_SIZE = 6
    TAGS_NUM = 5
    ENCODED_IMAGE = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///' \
                    '9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_get_recipes_endpoint(self, client, user_client, test_user):
        factories.RecipeFactory.create_batch(self.RECIPES_NUM)
        response = client.get(self.LIST_ENDPOINT)

        assert response.status_code != 404, (
            f'{self.LIST_ENDPOINT} not found, check url paths'
        )
        assert response.status_code == 200, (
            f'{self.LIST_ENDPOINT} must be available for unauthorized clients'
        )
        response = user_client.get(self.LIST_ENDPOINT)
        assert response.status_code == 200, (
            f'{self.LIST_ENDPOINT} must be available for authorized clients'
        )

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_recipes_pagination_and_fields(self, client):
        factories.RecipeFactory.create_batch(self.RECIPES_NUM)
        response = client.get(self.LIST_ENDPOINT)
        response_data = response.json()

        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, f'{self.LIST_ENDPOINT} returned data without pagination'
        assert type(response_data['results']) == list, (
            f'{self.LIST_ENDPOINT} returned inccorect data type for results parameter'
        )
        assert response_data['count'] == self.RECIPES_NUM, (
            f'{self.LIST_ENDPOINT} returned incorrect count value')
        assert len(response_data['results']) == self.PAGE_SIZE, (
            f'{self.LIST_ENDPOINT} must return {self.PAGE_SIZE} number of instances')

        # Test nested field types
        some_recipe = response_data['results'][0]
        tags = some_recipe.get('tags')
        author = some_recipe.get('author')
        ingredients = some_recipe.get('ingredients')

        assert isinstance(tags, list), (
            f'{self.LIST_ENDPOINT} must return tags as nested object(list)'
        )
        assert isinstance(author, dict), (
            f'{self.LIST_ENDPOINT} must return author as nested object(dict)'
        )
        assert isinstance(ingredients, list), (
            f'{self.LIST_ENDPOINT} must return ingredients as nested object(list)'
        )

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_create_recipe(self, client, user_client, test_user):
        num_recipe_objects = Recipe.objects.count()
        tags = factories.TagFactory.create_batch(self.TAGS_NUM)
        ingredients = []
        tags_ids = [tag.id for tag in tags]
        for _ in range(self.INGREDIENTS_NUM):
            ingredient = factories.IngredientFactory.create()
            ingredients.append({'id': ingredient.id, 'amount': random.randint(1, 30)})
        recipe = factories.RecipeFactory.build()
        encoded_image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///' \
                        '9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='
        data = {
            'author': test_user.id,
            'name': recipe.name,
            'image': encoded_image,
            'text': recipe.text,
            'tags': tags_ids,
            'ingredients': ingredients,
            'cooking_time': recipe.cooking_time,
            'created_date': recipe.created_date,
        }
        response = user_client.post(self.LIST_ENDPOINT, data=data, format='json')
        assert response.status_code == 201
        assert Recipe.objects.count() == num_recipe_objects + 1, (
            f'POST with correct data to {self.LIST_ENDPOINT} must create new recipe'
        )

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_add_recipe_to_favorites_or_shopping_cart(self, client, user_client, test_user):
        num_fav_objects = FavouriteRecipe.objects.filter(user=test_user).count()
        tags = factories.TagFactory.create_batch(self.TAGS_NUM)
        recipe = factories.RecipeFactory.create(tags=tags)
        recipe2 = factories.RecipeFactory.create(tags=tags[0])
        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/favorite/')

        assert response.status_code == 201
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'POST with correct data to {self.LIST_ENDPOINT}{recipe.id}/favorite/ must create new favoriteRecipe instance'
        )

        # Test is_favorited flag
        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/')
        favorite_status = response.json().get('is_favorited')
        shopping_cart_status = response.json().get('is_in_shopping_cart')

        assert favorite_status is True, (
            f'Check {self.LIST_ENDPOINT}{recipe.id}/favorite/ adds recipe to favorites'
        )
        assert shopping_cart_status is False, (
            f'Check {self.LIST_ENDPOINT}{recipe.id}/favorite/ doesnt change is_shopping_cart flag'
        )

        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe2.id}/')
        favorite_status = response.json().get('is_favorited')
        assert favorite_status is False, (
            f'Check {self.LIST_ENDPOINT}{recipe.id}/ with recipe not added to favorites shows False flag'
        )

        # Test is_in_shopping_cart flag
        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/shopping_cart/')

        assert response.status_code == 201, (
            f'Check {self.LIST_ENDPOINT}{recipe.id}/shopping_cart/ adds recipe to shopping cart '
        )
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'{self.LIST_ENDPOINT}{recipe.id}/favorite/ must not create new favoriteRecipe instance'
        )

        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/')
        shopping_cart_status = response.json().get('is_in_shopping_cart')
        assert shopping_cart_status is True, (
            f'Check {self.LIST_ENDPOINT}{recipe.id}/shopping_cart/ changes is_shopping_cart flag'
        )

        # Test delete from favorites
        response = user_client.delete(f'{self.LIST_ENDPOINT}{recipe.id}/favorite/')
        assert response.status_code == 204
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'{self.LIST_ENDPOINT}{recipe.id}/favorite/ shouldnt delete favRecipe instance with is_shopping_cart == True'
        )

        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/')
        favorite_status = response.json().get('is_favorited')
        assert favorite_status is False, (
            f'DELETE to {self.LIST_ENDPOINT}{recipe.id}/ changes favorite flag'
        )

        # Test delete from shopping_cart
        response = user_client.delete(f'{self.LIST_ENDPOINT}{recipe.id}/shopping_cart/')
        assert response.status_code == 204
        assert FavouriteRecipe.objects.filter(user=test_user).count() == 0, (
            f'{self.LIST_ENDPOINT}{recipe.id}/shopping_cart/ must delete favRecipe instance when status flags == False'
        )

        response = user_client.get(f'{self.LIST_ENDPOINT}{recipe.id}/')
        shopping_cart_status = response.json().get('is_in_shopping_cart')
        assert shopping_cart_status is False, (
            f'DELETE to {self.LIST_ENDPOINT}{recipe.id}/ changes shopping_cart flag'
        )

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe(self, client, user_client, test_user, test_user2):
        tags = factories.TagFactory.create_batch(self.TAGS_NUM)
        recipe_by_user = factories.RecipeFactory.create(tags=tags, author=test_user)
        recipe_by_user2 = factories.RecipeFactory.create(tags=tags[0], author=test_user2)

        num_recipes_by_user = Recipe.objects.filter(author=test_user).count()
        all_recipes = Recipe.objects.count()
        response = client.delete(f'{self.LIST_ENDPOINT}{recipe_by_user2.id}/')

        assert response.status_code == 401, (
            f'{self.LIST_ENDPOINT}{recipe_by_user2.id}/ must return 401 for unauthorized clients'
        )

        response = user_client.delete(f'{self.LIST_ENDPOINT}{recipe_by_user2.id}/')
        assert Recipe.objects.count() == all_recipes
        assert response.status_code == 403, (
            f'{self.LIST_ENDPOINT}{recipe_by_user2.id}/ - user cant delete recipe by another user'
        )

        response = user_client.delete(f'{self.LIST_ENDPOINT}{recipe_by_user.id}/')
        assert response.status_code == 204, (
            f'DELETE to {self.LIST_ENDPOINT} supposed to return 204'
        )
        assert Recipe.objects.filter(author=test_user).count() == num_recipes_by_user - 1, (
            f'DELETE to {self.LIST_ENDPOINT} must delete recipe instance'
        )

        # TODO: test update

def test_remove_temp_dir():
    try:
        shutil.rmtree(os.path.join(BASE_DIR, TEMP_DIR))
    except OSError as err:
        print(err)
