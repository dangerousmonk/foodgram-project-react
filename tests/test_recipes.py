import pytest
from . import factories
from foodgram.recipes.models import Recipe
import json

class TestTags:
    ENDPOINT = '/api/recipes/'
    _RECIPES_NUM = 8
    _INGREDIENTS_NUM = 4
    _PAGE_SIZE = 6
    _TAGS_NUM = 5

    @pytest.mark.django_db(transaction=True)
    def test_get_recipes_endpoint(self, client, user_client, test_user):
        #tags = factories.TagFactory.create_batch(5)
        #ingredients = factories.IngredientFactory.create_batch(5)
        #recipe_1 = factories.RecipeFactory.build()
        '''recipe_1.tags.add(*tags)
        print(recipe_1.name)
        print(recipe_1.author)
        print(recipe_1.image)
        print(recipe_1.text)
        print(recipe_1.tags.all())
        print(recipe_1.ingredients.all())
        print(recipe_1.created_date)
        print(recipe_1.cooking_time)
        assert False'''
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


    @pytest.mark.django_db(transaction=True)
    def test_recipes_pagination(self, client, user_client, test_user):
        '''recipe_1.tags.add(*tags)
        print(recipe_1.name)
        print(recipe_1.author)
        print(recipe_1.image)
        print(recipe_1.text)
        print(recipe_1.tags.all())
        print(recipe_1.ingredients.all())
        print(recipe_1.created_date)
        print(recipe_1.cooking_time)
        assert False'''
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

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe(self, client, user_client, test_user):
        tags = factories.TagFactory.create_batch(self._TAGS_NUM)
        ingr = factories.IngredientFactory.create()
        tags_ids = []
        for tag in tags:
            tags_ids.append(tag.id)
        ingredients = factories.IngredientFactory.create_batch(self._INGREDIENTS_NUM)
        recipe = factories.RecipeFactory.build()
        data = {
            'author': test_user.id,
            'name': recipe.name,
            #'image': recipe.image,
            'text': recipe.text,
            'tags': tags_ids,
            'ingredients': [{"id": ingr.id, "amount": 12}],
            'cooking_time': recipe.cooking_time,
            'created_date': recipe.created_date,
        }
        date_as_json = json.dumps(data)
        response = user_client.post(self.ENDPOINT, data=date_as_json, format='application/json')
        print(response)
        print(response.json())
        assert response.status_code == 403










