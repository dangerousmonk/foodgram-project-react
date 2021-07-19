from django.contrib.admin import ModelAdmin, register, site
from .models import MeasurementUnit, Ingredient
#from foodgram.recipes.admin import IngredientAmountInline


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)
    ordering = ('name',)
    empty_value_display = '-пусто-'

@register(MeasurementUnit)
class MeasurementUnit(ModelAdmin):
    list_display = ('name', 'metric')
    search_fields = ('name',)
    list_filter = ('name', 'metric',)
    ordering = ('name',)
    empty_value_display = '-пусто-'

