import json
from itertools import chain
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.core.serializers import serialize
from ..models import Ingredient
from ..views.cocktail_api import CocktailApi


class SearchView(View):

    @method_decorator(ensure_csrf_cookie)
    @method_decorator(csrf_protect)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            search_type = data.get('command', '')
            if search_type == 'search_cocktails':
                query = data.get('query', '')
                results = self.search_cocktails(query)
            elif search_type == 'search_ingredients':
                query = data.get('ingredients', '')
                results = self.search_ingredients(query)
            else:
                return JsonResponse({'error': 'Invalid search type'}, status=400)

            results = serialize('json', results)
            return JsonResponse({'cocktails':results}, safe=False, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    def useful(self, item):
        if item and len(item) == 1:
            result = item[0]
        elif item:
            result = list(chain(*item))
        else:
            result = []
        return result

    def api_useful(self, item):
        if not item:
            return []
        return item

    def search_cocktails(self, query):
        cocktail_api = CocktailApi()
        cocktails_api = self.api_useful(cocktail_api.api_search_by_name(query))
        cocktails_db = self.useful(cocktail_api.database_search_by_name(query))
        cocktails = cocktails_db + cocktails_api
        return cocktails


    def search_ingredients(self, query):
        cocktail_api = CocktailApi()
        cocktails_api = self.api_useful(cocktail_api.api_search_by_ingredient(query))
        cocktails_db = self.useful(cocktail_api.database_search_by_ingredient(query))
        cocktails = cocktails_db + cocktails_api
        return cocktails

def all_ingred(request):
    ingredients = Ingredient.objects.values_list('name', flat=True)
    return JsonResponse({'ingredients': list(ingredients)})
