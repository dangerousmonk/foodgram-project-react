from django.contrib.admin import ModelAdmin, register
from .models import MeasurementUnit, Ingredient


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)
    ordering = ('name',)
    empty_value_display = '-'


@register(MeasurementUnit)
class MeasurementUnit(ModelAdmin):
    list_display = ('id', 'name', 'metric')
    search_fields = ('name',)
    list_filter = ('name', 'metric',)
    ordering = ('name',)
    empty_value_display = '-'
