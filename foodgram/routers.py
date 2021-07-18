from rest_framework.routers import DefaultRouter

from foodgram.recipes.views import TagViewSet, RecipeViewSet, IngredientAmountViewSet
from foodgram.ingredients.views import IngredientViewSet
from foodgram.users.views import SubscriptionViewSet, CustomUserViewSet

v1_router = DefaultRouter()
# Recipes
v1_router.register(r'tags',TagViewSet, basename='tags')
v1_router.register(r'recipes',RecipeViewSet, basename='recipes')
v1_router.register(r'amounts',IngredientAmountViewSet, basename='amounts')
v1_router.register(r'ingredients',IngredientViewSet, basename='ingredients')
v1_router.register(r'users/subscriptions',SubscriptionViewSet, basename='subscriptions')
v1_router.register(r'users',CustomUserViewSet, basename='custom-users')

