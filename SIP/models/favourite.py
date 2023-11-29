from django.db import models
from django.contrib.auth.models import User


class FavouriteCocktail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cocktail = models.ForeignKey('SIP.Cocktail', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.cocktail.name}"


class FavouriteIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('SIP.Ingredient', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"
