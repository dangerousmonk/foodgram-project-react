import datetime
from random import randrange

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

import factory
import factory.fuzzy

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: f'username-{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@gmail.com')
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))
    first_name = factory.Sequence(lambda n: f'John-{n}')
    last_name = factory.Sequence(lambda n: f'Doe-{n}')


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


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipes.Recipe'
        strategy = factory.CREATE_STRATEGY

    author = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'recipe-{n}')
    text = factory.Sequence(lambda n: f'Description-{n}')
    image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'test.jpg'
        )
    )
    created_date = factory.LazyFunction(datetime.datetime.now)
    cooking_time = factory.fuzzy.FuzzyInteger(1, 50)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            try:
                for tag in extracted:
                    self.tags.add(tag)
            except TypeError:
                self.tags.add(extracted)


class IngredientAmountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipes.IngredientAmount'
        strategy = factory.CREATE_STRATEGY

    author = factory.SubFactory(UserFactory)
    name = factory.SubFactory(UserFactory)
    amount = factory.Iterator([randrange(1, 50)])


class MeasurementUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ingredients.MeasurementUnit'
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: f'measure-{n}')
    metric = factory.Iterator(['mass', 'volume', 'quantity'])


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ingredients.Ingredient'
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: f'ingredient-{n}')
    measurement_unit = factory.SubFactory(MeasurementUnitFactory)
