from django.contrib import admin
from .models import Tag, Ingredient, CocktailIngredient, Cocktail, Review, Star

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(CocktailIngredient)
admin.site.register(Cocktail)
admin.site.register(Review)
admin.site.register(Star)
