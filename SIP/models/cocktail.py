from django.db import models
from django.utils import timezone


class Cocktail(models.Model):
    CREATE_BY = (
        ('o', 'Official'),
        ('u', 'Unofficial')
    )
    name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    cocktail_tag = models.CharField(max_length=1, choices=CREATE_BY)  # 'o' for official, 'u' for unofficial
    tags = models.ManyToManyField('SIP.Tag', blank=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    glass = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField('SIP.Ingredient', through='SIP.CocktailIngredient', blank=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    image_source = models.URLField(max_length=255, blank=True, null=True)
    image_attribution = models.CharField(max_length=255, blank=True, null=True)
    date_modified = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name
