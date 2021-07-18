import factory
from django.conf import settings
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: f'username-{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@gmail.com')
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))
    first_name = factory.Sequence(lambda n: f'John-{n}')
    last_name =  factory.Sequence(lambda n: f'Doe-{n}')

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipes.Tag'
        strategy = factory.CREATE_STRATEGY

    color = factory.Sequence(lambda n: f'#8775D{n}')
    name = factory.Sequence(lambda n: f'tag-{n}')

    slug = factory.Sequence(lambda n: f'slug-{n}')

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.UserSubscription'
        strategy = factory.CREATE_STRATEGY

    subscriber = factory.SubFactory(UserFactory)
    subscription = factory.SubFactory(UserFactory)
