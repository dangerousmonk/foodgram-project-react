from django.contrib import admin
from . import models
from foodgram.recipes.admin import IngredientAmountInline

admin.site.register(models.MeasurementUnit)

@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountInline]

