import pytest
from . import factories


class TestTags:
    ENDPOINT = '/api/tags/'
    TAGS_NUM = 10

    @pytest.mark.django_db(transaction=True)
    def test_get_tag(self, client, user_client):
        factories.TagFactory.create_batch(self.TAGS_NUM)
        response = client.get(self.ENDPOINT)
        assert response.status_code != 404, f'{self.ENDPOINT} doesnt exist'
        assert response.status_code == 200, f'{self.ENDPOINT} must be available for un-authorized clients'
        reponse_data = response.json()
        assert len(reponse_data) == self.TAGS_NUM, f'{self.ENDPOINT} must return all tags'

        data = {}
        response = user_client.post(self.ENDPOINT, data=data)
        assert response.status_code == 405, f'POST to {self.ENDPOINT} not avilable'

    @pytest.mark.django_db(transaction=True)
    def test_retreive_tag(self, client, user_client):
        tag = factories.TagFactory.create()
        response = client.get(f'{self.ENDPOINT}{tag.id}/')
        assert response.status_code == 200, (
            'Tag detail route must be available for unauthorized clients'
        )
        expected_json = {
            'name': tag.name,
            'slug': tag.slug,
            'color': tag.color,
            'id': tag.id
        }
        assert response.json() == expected_json, (
            f'{self.ENDPOINT}{tag.id}/ must return correct data for tag instance'
        )
        response = client.get(f'{self.ENDPOINT}{10}/')
        assert response.status_code == 404, (
            'Lookup for non-existent tag instance must return 404'
        )
