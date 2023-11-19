from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from SIP.views.cocktail_api import CocktailApi
from ..models import Star, Cocktail, Ingredient


class IndexView(View):
    template_name = 'sip/index.html'

    def get(self, request):
        cocktail_api = CocktailApi()
        cocktails = Cocktail.objects.all()
        ingredients = Ingredient.objects.all()
        search_query = request.GET.get('search')
        search_type = request.GET.get('search_type')

        if search_query and search_type:
            if search_type == 'cocktail' and Cocktail.objects.filter(
                    name__icontains=search_query).exists():
                cocktails = Cocktail.objects.filter(name__icontains=search_query)
                ingredients = []
            elif search_type == 'ingredient' and Ingredient.objects.filter(
                    name__icontains=search_query).exists():
                ingredients = Ingredient.objects.filter(name__icontains=search_query)
                cocktails = []
            else:
                cocktails = []
                ingredients = []

        if cocktails is not None:
            for cocktail in cocktails:
                cocktail.average_score = self.calculate_star_rating(cocktail)
            context = {
                'cocktails': cocktails,
                'ingredients': ingredients,
                'search_type': search_type,
                'search_query': search_query,
            }
        else:
            return render(request, self.template_name)

        return render(request, self.template_name, context)

    def calculate_star_rating(self, cocktail):
        # Customize this function based on your design for star ratings
        average_score = Star.objects.filter(cocktail=cocktail).aggregate(Avg('score'))['score__avg']

        if average_score is not None:
            digit = int(average_score)
            integer_part = [1] * digit
            fractional_part = average_score - digit
            if fractional_part == 0:
                fractional_part = None
            return integer_part, fractional_part
        else:
            return None
