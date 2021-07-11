from django.contrib import admin
from .models import Recipe, Tag, Ingredient, MeasurementUnit, IngredientAmount

admin.site.register(Tag)

admin.site.register(IngredientAmount)
admin.site.register(MeasurementUnit)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountInline]


@admin.register(Ingredient)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountInline]
