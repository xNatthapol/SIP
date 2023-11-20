from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from SIP.views.cocktail_api import CocktailApi
from ..models import Star, Cocktail, Ingredient


class IndexView(View):
    template_name = 'sip/index.html'

    def get(self, request):
        cocktails = Cocktail.objects.all()
        ingredients = Ingredient.objects.all()

        if cocktails is not None:
            for cocktail in cocktails:
                cocktail.average_score = self.calculate_star_rating(cocktail)
            context = {
                'cocktails': cocktails,
                'ingredients': ingredients,
                'search_type': 'cocktail',

            }
        else:
            return render(request, self.template_name)

        return render(request, self.template_name, context)

    def post(self, request):
        cocktail_api = CocktailApi()
        search_query = request.POST.get('search')
        search_type = request.POST.get('search_type')
        search_by = request.POST.get('search_by')
        cocktails = []

        if search_by == 'api':
            if search_type == 'cocktail':
                cocktails = cocktail_api.get_cocktail_by_name(search_query)
            elif search_type == 'ingredient':
                ingredients = cocktail_api.get_ingredient_by_name(search_query)
                print('ingredients: ', ingredients)
                return render(request, self.template_name, {'ingredients': ingredients, 'search_type': search_type})
        elif search_by == 'db':
            if search_type == 'cocktail':
                cocktails = Cocktail.objects.filter(name__icontains=search_query)
            elif search_type == 'ingredient':
                ingredients = Ingredient.objects.filter(name__icontains=search_query)
                print('ingredients: ', ingredients)
                return render(request, self.template_name, {'ingredients': ingredients, 'search_type': search_type})

        print('cocktails: ', cocktails)

        if cocktails is not None:
            for cocktail in cocktails:
                cocktail.average_score = self.calculate_star_rating(cocktail)

        context = {
                'cocktails': cocktails,
                'search_type': search_type,
                }

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
