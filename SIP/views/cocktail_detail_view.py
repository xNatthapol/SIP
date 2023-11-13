# views.py
from django.db.models import Avg
from django.shortcuts import render
from django.views import View
from ..models import Cocktail, Review, Star


class MyCocktailView(View):
    template_name = 'sip/cocktail_detail.html'

    def get(self, request, pk):
        cocktail = Cocktail.objects.get(pk=pk)

        # Fetch reviews for the cocktail
        reviews = Review.objects.filter(cocktail=cocktail)

        # Calculate average score for the cocktail
        average_score = Star.objects.filter(cocktail=cocktail).aggregate(Avg('score'))['score__avg']

        rating = self.calculate_star_rating(average_score)

        context = {
            'cocktail': cocktail,
            'star_rating': rating,
            'reviews': reviews,
            'average_score': average_score,
        }

        return render(request, self.template_name, context)

    def calculate_star_rating(self, average_score):
        # Customize this function based on your design for star ratings
        if average_score is not None:
            integer_part = int(average_score)
            fractional_part = average_score - integer_part
            return integer_part, fractional_part
        else:
            return None
