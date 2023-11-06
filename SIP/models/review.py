from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Review(models.Model):
    id_drink = models.IntegerField()
    tag = models.CharField(max_length=1)  # 'o' for official, 'u' for unofficial
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    reviewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sip_review'
    
    def __str__(self):
        return self.message

class Star(models.Model):
    id_drink = models.IntegerField()
    tag = models.CharField(max_length=1)  # 'o' for official, 'u' for unofficial
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        db_table = 'sip_star'

    def __str__(self):
        return self.score