from django.db import models


class Cocktails(models.Model):
    id_drink = models.IntegerField(primary_key=True)
    drink_name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    catalog = models.CharField(max_length=255)
    glass = models.CharField(max_length=255)
    instructions = models.TextField()
    ingredients = models.JSONField()
    image = models.URLField(max_length=255, blank=True, null=True)
    image_source = models.URLField(max_length=255, blank=True, null=True)
    image_attribution = models.CharField(max_length=255, blank=True, null=True)
    date_modified = models.DateTimeField()

    class Meta:
        abstract = True


class OfficialCocktails(Cocktails):
    class Meta:
        db_table = 'official_cocktails'


class UnofficialCocktails(Cocktails):
    class Meta:
        db_table = 'unofficial_cocktails'
