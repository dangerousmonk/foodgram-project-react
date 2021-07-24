import random
import shutil

from django.test import override_settings

import pytest

from foodgram.recipes.models import FavouriteRecipe, Recipe

from . import factories

TEMP_DIR = 'test_files'


class TestRecipes:
    # status flags -> is_in_shopping_cart & is_favorited
    _ENDPOINT = '/api/recipes/'
    _RECIPES_NUM = 8
    _INGREDIENTS_NUM = 4
    _PAGE_SIZE = 6
    _TAGS_NUM = 5
    _encoded_image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///' \
                     '9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_get_recipes_endpoint(self, client, user_client, test_user):
        factories.RecipeFactory.create_batch(self._RECIPES_NUM)
        response = client.get(self._ENDPOINT)
        assert response.status_code != 404, (
            f'{self._ENDPOINT} not found, check url paths'
        )
        assert response.status_code == 200, (
            f'{self._ENDPOINT} must be available for unauthorized clients'
        )
        response = user_client.get(self._ENDPOINT)
        assert response.status_code == 200, (
            f'{self._ENDPOINT} must be available for authorized clients'
        )

        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_recipes_pagination_and_fields(self, client, user_client, test_user):
        factories.RecipeFactory.create_batch(self._RECIPES_NUM)
        response = client.get(self._ENDPOINT)
        response_data = response.json()
        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, f'{self._ENDPOINT} returned data without pagination'
        assert type(response_data['results']) == list, (
            f'{self._ENDPOINT} returned inccorect data type for results parameter'
        )
        assert response_data['count'] == self._RECIPES_NUM, (
            f'{self._ENDPOINT} returned incorrect count value')
        assert len(response_data['results']) == self._PAGE_SIZE, (
            f'{self._ENDPOINT} must return {self._PAGE_SIZE} number of instances')

        # Test nested field types
        some_recipe = response_data['results'][0]
        tags = some_recipe.get('tags')
        author = some_recipe.get('author')
        ingredients = some_recipe.get('ingredients')
        assert isinstance(tags, list), (
            f'{self._ENDPOINT} must return tags as nested object(list)'
        )
        assert isinstance(author, dict), (
            f'{self._ENDPOINT} must return author as nested object(dict)'
        )
        assert isinstance(ingredients, list), (
            f'{self._ENDPOINT} must return ingredients as nested object(list)'
        )

        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_create_recipe(self, client, user_client, test_user):
        num_recipe_objects = Recipe.objects.count()
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        ingredients = []
        tags_ids = [tag.id for tag in tags]
        for _ in range(self._INGREDIENTS_NUM):
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
        response = user_client.post(self._ENDPOINT, data=data, format='json')
        assert response.status_code == 201
        assert Recipe.objects.count() == num_recipe_objects + 1, (
            f'POST with correct data to {self._ENDPOINT} must create new recipe'
        )
        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_add_recipe_to_favorites_or_shopping_cart(self, client, user_client, test_user):
        num_fav_objects = FavouriteRecipe.objects.filter(user=test_user).count()
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        recipe = factories.RecipeFactory.create(tags=tags)
        recipe2 = factories.RecipeFactory.create(tags=tags[0])
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/favorite/')
        assert response.status_code == 201
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'POST with correct data to {self._ENDPOINT}{recipe.id}/favorite/ must create new favoriteRecipe instance'
        )

        # Test is_favorited flag
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/')
        favorite_status = response.json().get('is_favorited')
        shopping_cart_status = response.json().get('is_in_shopping_cart')
        assert favorite_status == True, (
            f'Check {self._ENDPOINT}{recipe.id}/favorite/ adds recipe to favorites'
        )
        assert shopping_cart_status == False, (
            f'Check {self._ENDPOINT}{recipe.id}/favorite/ doesnt change is_shopping_cart flag'
        )

        response = user_client.get(f'{self._ENDPOINT}{recipe2.id}/')
        favorite_status = response.json().get('is_favorited')
        assert favorite_status == False, (
            f'Check {self._ENDPOINT}{recipe.id}/ with recipe not added to favorites shows False flag'
        )

        # Test is_in_shopping_cart flag
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/shopping_cart/')
        assert response.status_code == 201, (
            f'Check {self._ENDPOINT}{recipe.id}/shopping_cart/ adds recipe to shopping cart '
        )
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'{self._ENDPOINT}{recipe.id}/favorite/ must not create new favoriteRecipe instance'
        )
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/')
        shopping_cart_status = response.json().get('is_in_shopping_cart')
        assert shopping_cart_status == True, (
            f'Check {self._ENDPOINT}{recipe.id}/shopping_cart/ changes is_shopping_cart flag'
        )

        # Test delete from favorites
        response = user_client.delete(f'{self._ENDPOINT}{recipe.id}/favorite/')
        assert response.status_code == 204
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'{self._ENDPOINT}{recipe.id}/favorite/ shouldnt delete favRecipe instance with is_shopping_cart == True'
        )
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/')
        favorite_status = response.json().get('is_favorited')
        assert favorite_status == False, (
            f'DELETE to {self._ENDPOINT}{recipe.id}/ changes favorite flag'
        )

        # Test delete from shopping_cart
        response = user_client.delete(f'{self._ENDPOINT}{recipe.id}/shopping_cart/')
        assert response.status_code == 204
        assert FavouriteRecipe.objects.filter(user=test_user).count() == 0, (
            f'{self._ENDPOINT}{recipe.id}/shopping_cart/ must delete favRecipe instance when status flags == False'
        )
        response = user_client.get(f'{self._ENDPOINT}{recipe.id}/')
        shopping_cart_status = response.json().get('is_in_shopping_cart')
        assert shopping_cart_status == False, (
            f'DELETE to {self._ENDPOINT}{recipe.id}/ changes shopping_cart flag'
        )

        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe(self, client, user_client, user2_client, test_user, test_user2):
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        recipe_by_user = factories.RecipeFactory.create(tags=tags, author=test_user)
        recipe_by_user2 = factories.RecipeFactory.create(tags=tags[0], author=test_user2)
        num_recipes_by_user = Recipe.objects.filter(author=test_user).count()
        all_recipes = Recipe.objects.count()

        response = client.delete(f'{self._ENDPOINT}{recipe_by_user2.id}/')
        assert response.status_code == 401, (
            f'{self._ENDPOINT}{recipe_by_user2.id}/ must return 401 for unauthorized clients'
        )

        response = user_client.delete(f'{self._ENDPOINT}{recipe_by_user2.id}/')
        assert Recipe.objects.count() == all_recipes
        assert response.status_code == 403, (
            f'{self._ENDPOINT}{recipe_by_user2.id}/ - user cant delete recipe by another user'
        )

        response = user_client.delete(f'{self._ENDPOINT}{recipe_by_user.id}/')
        assert response.status_code == 204, (
            f'DELETE to {self._ENDPOINT} supposed to return 204'
        )
        assert Recipe.objects.filter(author=test_user).count() == num_recipes_by_user - 1, (
            f'DELETE to {self._ENDPOINT} must delete recipe instance'
        )

        # TODO: test update

        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)
