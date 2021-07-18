import pytest
from . import factories
from foodgram.users.models import UserSubscription


class TestTags:
    ENDPOINT = '/api/users/subscriptions/'

    @pytest.mark.django_db(transaction=True)
    def test_get_subscriptions(self, client, user_client, test_user):
        user_1 = factories.UserFactory()
        user_2 = factories.UserFactory()
        factories.SubscriptionFactory.create(subscriber=user_1, subscription=user_2)
        response = client.get(self.ENDPOINT)
        assert response.status_code != 404, f'{self.ENDPOINT} doesnt exist'
        assert response.status_code == 401, f'{self.ENDPOINT} not available for un-authorized clients'

        response = user_client.get(self.ENDPOINT)
        response_data = response.json()
        assert response_data.get('count') == 0, (
            f'{self.ENDPOINT} must return empty results for user without subscriptions'
        )

        factories.SubscriptionFactory.create(subscriber=test_user, subscription=user_1)
        factories.SubscriptionFactory.create(subscriber=test_user, subscription=user_2)
        response = user_client.get(self.ENDPOINT)
        response_data = response.json()
        assert response.status_code == 200, (
            f'{self.ENDPOINT} must return 200 for authorized clients'
        )
        assert response_data.get('count') == 2, (
            f'{self.ENDPOINT} must return only users subscriptions'
        )

        # Test pagination
        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, f'{self.ENDPOINT} must return data with pagination'
        assert type(response_data.get('results')) == list, (
            f'{self.ENDPOINT} returned inccorect data type for results parameter'
        )
        assert response_data.get('count') == 2, (
            f'{self.ENDPOINT} returned incorrect number of subscriptions instances')

        # Test fields
        instance_data = response_data.get('results')[0]
        assert 'email' in instance_data
        assert 'id' in instance_data
        assert 'username' in instance_data
        assert 'first_name' in instance_data
        assert 'last_name' in instance_data
        assert 'is_subscribed' in instance_data
        assert 'recipes' in instance_data
        assert 'recipes_count' in instance_data, (
            f'{self.ENDPOINT} must return correct fields in response'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_and_subscribed_flag(self, client, user_client, test_user):
        user_1 = factories.UserFactory()
        response = client.get(f'/api/users/{user_1.id}/subscribe/')
        assert response.status_code == 401, (
            'Check api/users/{user_id}/subscribe/ not available for unauthorized users'
        )

        all_subscriptions = UserSubscription.objects.count()
        response = user_client.get(f'/api/users/{user_1.id}/subscribe/')  # Front expects GET request
        assert response.status_code != 404, (
            'Check api/users/{user_id}/subscribe/ included in url config'
        )
        assert UserSubscription.objects.count() == all_subscriptions + 1
        assert response.status_code == 201, (
            'Check api/users/{user_id}/subscribe/ must create new subscription instance'
        )
        response = user_client.get(f'/api/users/{user_1.id}/subscribe/')
        assert response.status_code == 400, (
            'Cant subscribe to the user twice'
        )
        assert UserSubscription.objects.count() == all_subscriptions + 1, (
            'Cant subscribe to the user twice'
        )
        response = user_client.get(f'/api/users/{test_user.id}/subscribe/')
        assert response.status_code == 400, 'User cant subscribe to himself'
        response = user_client.get(f'/api/users/{user_1.id}/')
        response_data = response.json()
        assert response_data.get('is_subscribed') == True, (
            '/api/users/{user_id}/subscribe/ must change is_subscribed flag'
        )
    @pytest.mark.xfail
    @pytest.mark.django_db(transaction=True)
    def test_delete_subscription(self, client, user_client, test_user):
        user_1 = factories.UserFactory()
        response = user_client.get(f'/api/users/{user_1.id}/subscribe/')
        all_subscriptions = UserSubscription.objects.count()
        print(response.json())
        response = user_client.delete(f'/api/users/{user_1.id}/subscribe/')
        print(response.json())
        assert response.status_code == 400

