from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from SIP.views.cocktail_api import CocktailApi
from ..models import Star


class IndexView(View):
    template_name = 'sip/index.html'

    def get(self, request):
        cocktail_api = CocktailApi()
        search_cocktail = request.GET.get('search')
        if search_cocktail:
            cocktails = cocktail_api.get_cocktail_by_name(search_cocktail)
        else:
            cocktails = cocktail_api.get_cocktail_by_name('negroni')

        for cocktail in cocktails:
            cocktail.average_score = self.calculate_star_rating(cocktail)

        return render(request, self.template_name,
                      context={'cocktails': cocktails,
                               'search_query': search_cocktail})

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
