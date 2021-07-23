import pytest
from django.contrib.auth import get_user_model

from . import factories


class TestUsers:
    ENDPOINT = '/api/users/'
    CURRENT_USER = '/api/users/me/'
    USERS_NUM = 8



    @pytest.mark.django_db(transaction=True)
    def test_get_endpoint(self,client,user_client):
        response = client.get(self.ENDPOINT)
        assert response.status_code != 404, f'Endpoint {self.ENDPOINT} doesnt exist'
        assert response.status_code == 200, f'Endpoint {self.ENDPOINT} available for un-authorized clients'

        response = user_client.get(self.ENDPOINT)
        assert response.status_code != 404, f'Endpoint {self.ENDPOINT} doesnt exist'
        assert response.status_code == 200, f'Endpoint {self.ENDPOINT} available for authorized clients'


    @pytest.mark.django_db(transaction=True)
    def test_register_user(self,client):
        user = factories.UserFactory.build()
        data = {
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        user_count = get_user_model().objects.count()
        response = client.post(self.ENDPOINT, data=data)

        assert response.status_code == 201, (
            f'POST to {self.ENDPOINT} with valid data must create new user'
        )
        assert user_count + 1 == get_user_model().objects.count(), (
            f'Check {self.ENDPOINT} creates new user instance'
        )
        assert response.status_code != 400, f'Check fields data sent to {self.ENDPOINT}'

        response_data = response.json()
        print(data)
        assert response_data.get('username') == data.get('username'), (
            f'{self.ENDPOINT} returned no username in response'
        )
        assert response_data.get('first_name') == data.get('first_name'), (
            f'{self.ENDPOINT} returned no first_name in response'
        )
        assert response_data.get('last_name') == data.get('last_name'), (
            f'{self.ENDPOINT} returned no last_name in response'
        )
        assert response_data.get('email') == data.get('email'), (
            f'{self.ENDPOINT} returned no email in response'
        )

        data['username'] = 'Anotheruser'
        data['first_name'] = 'another_name'
        data['last_name'] = 'another_last'

        response = client.post(self.ENDPOINT, data=data)
        assert response.status_code == 400, f'{self.ENDPOINT} - User email must be unique'

        data = {}
        response = client.post(self.ENDPOINT, data=data)
        assert response.status_code == 400, f'POST to {self.ENDPOINT} with invalid data must return 400'


    @pytest.mark.django_db(transaction=True)
    def test_users_endpoint_pagination(self, client):
        factories.UserFactory.create_batch(self.USERS_NUM)
        response = client.get(self.ENDPOINT).json()
        assert 'count' in response
        assert 'next' in response
        assert 'previous' in response
        assert 'results' in response, f'{self.ENDPOINT} returned data without pagination'
        assert type(response['results']) == list, (
            f'{self.ENDPOINT} returned inccorect data type for results parameter'
        )
        assert response['count'] == self.USERS_NUM, (
            f'{self.ENDPOINT} returned incorrect number of user instances')

    @pytest.mark.django_db(transaction=True)
    def test_user_profile(self, client,user_client):
        user = factories.UserFactory.create()
        response = client.get(f'{self.ENDPOINT}{user.id}/')
        assert response.status_code != 404, (
            'User profile page not available, check urls config'
        )
        assert response.status_code == 401, 'Unauthorized clients cant see user profile page'

        response = user_client.get(f'{self.ENDPOINT}{user.id}/')
        assert response.status_code == 200, 'User profile available for authorized clients'

    @pytest.mark.django_db(transaction=True)
    def test_current_user(self, client, user_client,test_user):
        user = factories.UserFactory.create()
        response = client.get(self.CURRENT_USER)
        assert response.status_code != 404, (
            f'Endpoint {self.CURRENT_USER} doesnt exist'
        )
        assert response.status_code == 401, (
            f'{self.CURRENT_USER} not available for unauthorized clients'
        )

        response = user_client.get(self.CURRENT_USER)
        response_data = response.json()
        assert response.status_code == 200, (
            f'{self.CURRENT_USER} must be available for authorized clients'
        )
        assert response_data.get('username') == test_user.username, (
            f'{self.CURRENT_USER} returned incorrect username'
        )
        assert response_data.get('first_name') == test_user.first_name, (
            f'{self.CURRENT_USER} returned incorrect first_name'
        )
        assert response_data.get('last_name') == test_user.last_name, (
            f'{self.CURRENT_USER} returned incorrect last_name'
        )
        assert response_data.get('email') == test_user.email, (
            f'{self.CURRENT_USER} returned incorrect email'
        )
        assert response_data.get('id') == test_user.id, (
            f'{self.CURRENT_USER} returned incorrect id'
        )









