from django.db import models

class Review(models.Model):
    star = models.ForeignKey("Star", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

class Star(models.Model):
    id_user = models.IntegerField(max_length=10)
    id_drink = models.IntegerField(max_length=10)
    tag = models.CharField(max_length=50)
    score = models.IntegerField()
