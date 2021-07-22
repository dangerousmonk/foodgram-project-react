from django.contrib.admin import ModelAdmin, register, site, display
from .models import Tag, Recipe, FavouriteRecipe, IngredientAmount
from django.utils.translation import gettext_lazy as _

site.register(IngredientAmount)
site.register(FavouriteRecipe)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color',)
    ordering = ('name',)
    empty_value_display = '-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('author', 'name', 'text', 'get_tags', 'created_date', 'image', 'cooking_time', 'get_favorites')
    filter_horizontal = ('tags',)
    search_fields = ('author',)
    list_filter = ('author', 'name', 'tags', 'ingredients', 'cooking_time')
    ordering = ('created_date', 'author')
    empty_value_display = '-'

    @display(description=_('Теги'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    @display(description=_('Added to favorites,number'))
    def get_favorites(self, obj):
        qs = obj.in_favourites.count()
        if qs:
            return qs
