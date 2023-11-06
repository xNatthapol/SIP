from django.db import models
from django.contrib.postgres import fields


class Cocktails(models.Model):
    drink_name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    tags = fields.ArrayField(
        models.CharField(max_length=255, blank=True, null=True),
        blank=True, null=True
    )
    catalog = models.CharField(max_length=255, blank=True, null=True)
    glass = models.CharField(max_length=255)
    instructions = models.TextField()
    ingredients = models.JSONField(default=dict)
    image = models.URLField(max_length=255, blank=True, null=True)
    image_source = models.URLField(max_length=255, blank=True, null=True)
    image_attribution = models.CharField(max_length=255, blank=True, null=True)
    date_modified = models.DateTimeField()

    class Meta:
        abstract = True


class Official(Cocktails):
    id_drink = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'official_cocktails'


class Unofficial(Cocktails):
    id_drink = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'unofficial_cocktails'
