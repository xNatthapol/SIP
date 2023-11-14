from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from SIP.views.cocktail_api import CocktailApi
from ..models import Star, Cocktail


class IndexView(View):
    template_name = 'sip/index.html'

    def get(self, request):
        cocktail_api = CocktailApi()
        cocktails = Cocktail.objects.all()
        search_cocktail = request.GET.get('search')
        if search_cocktail:
            if Cocktail.objects.filter(name__icontains=search_cocktail).exists():
                cocktails = Cocktail.objects.filter(name__icontains=search_cocktail)
            else:
                cocktails = cocktail_api.get_cocktail_by_name(search_cocktail)
        if cocktails is not None:
            for cocktail in cocktails:
                cocktail.average_score = self.calculate_star_rating(cocktail)
            content = {
                'cocktails': cocktails,
            }
        else:
            return render(request, self.template_name)
        return render(request, self.template_name, content)

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
