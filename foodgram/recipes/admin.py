from django.contrib import admin
from . import models

admin.site.register(models.Tag)
admin.site.register(models.IngredientAmount)
admin.site.register(models.Favourites)


class IngredientAmountInline(admin.TabularInline):
    model = models.IngredientAmount
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountInline]