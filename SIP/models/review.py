from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    cocktail = models.ForeignKey('SIP.Cocktail', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    reviewed_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return len(self.message) <= 255
    
    def __str__(self):
        return self.message


class Star(models.Model):
    cocktail = models.ForeignKey('SIP.Cocktail', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    rated_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return 1 <= self.score <= 5

    def __str__(self):
        return str(self.score)
