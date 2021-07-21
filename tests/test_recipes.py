import pytest
from . import factories
from foodgram.recipes.models import Recipe, FavouriteRecipe
import random
from django.test import override_settings
import shutil

TEMP_DIR = 'test_files'


class TestRecipes:
    _ENDPOINT = '/api/recipes/'
    _RECIPES_NUM = 8
    _INGREDIENTS_NUM = 4
    _PAGE_SIZE = 6
    _TAGS_NUM = 5

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

        #Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_recipes_pagination(self, client, user_client, test_user):
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
            ingredients.append({'id': ingredient.id, 'amount': random.randint(1,30)})
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
        response = user_client.get(self._ENDPOINT)
        print(response.json())
        assert False

    @override_settings(MEDIA_ROOT=(TEMP_DIR + '/media'))
    @pytest.mark.django_db(transaction=True)
    def test_add_recipe_to_favorites(self, client, user_client, test_user):
        num_fav_objects = FavouriteRecipe.objects.filter(user=test_user).count()
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        recipe1 = factories.RecipeFactory.create(tags=tags)
        recipe2 = factories.RecipeFactory.create()
        response = user_client.get(f'{self._ENDPOINT}{recipe1.id}/favorite/')
        assert response.status_code == 201
        assert FavouriteRecipe.objects.filter(user=test_user).count() == num_fav_objects + 1, (
            f'POST with correct data to {self._ENDPOINT}{recipe1.id}/favorite/ must create new favoriteRecipe object'
        )

       #Check is_favorited flag
        response = user_client.get(f'{self._ENDPOINT}{recipe1.id}/')
        favorite_status = response.json().get('is_favorited')
        assert favorite_status == True, (
            f'Check {self._ENDPOINT}{recipe1.id}/favorite/ adds recipe to favorites'
        )


        # Cleanup tmp dir for uploads
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError as err:
            print(err)
        assert False



