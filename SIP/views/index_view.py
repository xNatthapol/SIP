from django.shortcuts import render
from django.views import View
from SIP.views.cocktail_api import CocktailApi

class IndexView(View):
    template_name = 'sip/index.html'

    def get(self, request):
        cocktail_api = CocktailApi()
        search_cocktail = request.GET.get('search')
        if search_cocktail:
            cocktails = cocktail_api.get_cocktail_by_name(search_cocktail)
        else:
            cocktails = cocktail_api.get_cocktail_by_name('negroni')
        return render(request, self.template_name, context={'cocktails': cocktails, 'search_query': search_cocktail})
