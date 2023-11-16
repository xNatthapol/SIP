from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    

class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey('SIP.Cocktail', on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    measure = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.measure + ' ' + str(self.ingredient)
