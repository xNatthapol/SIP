from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from SIP.views.cocktail_api import CocktailApi
from ..models import Star, Cocktail, Ingredient


class IndexView(View):
    template_name = 'sip/index.html'
    # api = CocktailApi()

    def get(self, request):
        cocktails = self.calculate_star_rating(Cocktail.objects.order_by('-id')[:10])
        # random = self.calculate_star_rating(self.api.get_random_cocktails())
        ingredients = Ingredient.objects.order_by('-id')[:10]

        context = {
            'cocktails': cocktails,
            'ingredients': ingredients,
            # 'randoms': random,
        }
        return render(request, self.template_name, context)


    def calculate_star_rating(self, cocktails):
        for cocktail in cocktails:
            average_score = Star.objects.filter(cocktail=cocktail).aggregate(Avg('score'))['score__avg']
            if average_score:
                cocktail.star_rating = average_score
        return cocktails
