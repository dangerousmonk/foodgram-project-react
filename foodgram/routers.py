from rest_framework.routers import DefaultRouter

from foodgram.ingredients.views import IngredientViewSet
from foodgram.recipes.views import RecipeViewSet, TagViewSet
from foodgram.users.views import CustomUserViewSet, SubscriptionViewSet

v1_router = DefaultRouter()
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(
    r'users/subscriptions',
    SubscriptionViewSet,
    basename='subscriptions'
)
v1_router.register(r'users', CustomUserViewSet, basename='custom-users')
