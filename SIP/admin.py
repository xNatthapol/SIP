from django.contrib import admin
from .models import Official, Unofficial, Review, Star

admin.site.register(Official)
admin.site.register(Unofficial)
admin.site.register(Review)
admin.site.register(Star)
