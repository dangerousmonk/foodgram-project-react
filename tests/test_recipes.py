import pytest
from . import factories
from foodgram.recipes.models import Recipe
import random
from django.test import override_settings
import shutil

TEMP_DIR = 'test_files'


class TestRecipes:
    ENDPOINT = '/api/recipes/'
    _RECIPES_NUM = 8
    _INGREDIENTS_NUM = 4
    _PAGE_SIZE = 6
    _TAGS_NUM = 5

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_get_recipes_endpoint(self, client, user_client, test_user):
        factories.RecipeFactory.create_batch(self._RECIPES_NUM)
        response = client.get(self.ENDPOINT)
        assert response.status_code != 404, (
            f'{self.ENDPOINT} not found, check url paths'
        )
        assert response.status_code == 200, (
            f'{self.ENDPOINT} must be available for unauthorized clients'
        )
        response = user_client.get(self.ENDPOINT)
        assert response.status_code == 200, (
            f'{self.ENDPOINT} must be available for authorized clients'
        )

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_recipes_pagination(self, client, user_client, test_user):
        factories.RecipeFactory.create_batch(self._RECIPES_NUM)
        response = client.get(self.ENDPOINT)
        response_data = response.json()
        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, f'{self.ENDPOINT} returned data without pagination'
        assert type(response_data['results']) == list, (
            f'{self.ENDPOINT} returned inccorect data type for results parameter'
        )
        assert response_data['count'] == self._RECIPES_NUM, (
            f'{self.ENDPOINT} returned incorrect count value')
        assert len(response_data['results']) == self._PAGE_SIZE, (
            f'{self.ENDPOINT} must return {self._PAGE_SIZE} number of instances')

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_create_recipe(self, client, user_client, test_user):
        num_db_objects = Recipe.objects.count()
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        tags_ids, ingredients = [], []
        for tag in tags:
            tags_ids.append(tag.id)
        for _ in range(self._INGREDIENTS_NUM):
            ingredient = factories.IngredientFactory.create()
            amount = random.randint(1, 30)
            ingredients.append({'id': ingredient.id, 'amount': amount})
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
        response = user_client.post(self.ENDPOINT, data=data, format='json')
        assert response.status_code == 201
        assert Recipe.objects.count() == num_db_objects + 1, (
            f'POST with correct data to {self.ENDPOINT} must create new recipe'
        )

        print(response.json())
        assert False





def delete_temp_dir():
    try:
        shutil.rmtree(TEMP_DIR)
    except OSError:
        pass


delete_temp_dir()
