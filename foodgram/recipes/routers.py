from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet, IngredientAmountViewSet

v1_router = DefaultRouter()
v1_router.register(r'tags',TagViewSet, basename='tags')
v1_router.register(r'recipes',RecipeViewSet, basename='recipes')
v1_router.register(r'amounts',IngredientAmountViewSet, basename='amounts')