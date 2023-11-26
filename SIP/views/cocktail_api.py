import json

import requests
from datetime import datetime
from django.utils import timezone
from SIP.models import Tag, Ingredient, CocktailIngredient, Cocktail
from decouple import config
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

class CocktailApi:
    def __init__(self):
        self.base_url = config("API_KEY",default="https://www.thecocktaildb.com/api/json/v1/1/")

    def build_url(self, endpoint):
        return self.base_url + endpoint

    def dupicate_check(self, drink_name):
        cocktail = Cocktail.objects.filter(name__exact=drink_name,
                                           cocktail_tag__exact='o')
        if cocktail:
            return cocktail
        return None

    def ingred_dupicated(self, ingerd_name):
        ingredient = Ingredient.objects.filter(name__exact=ingerd_name)
        if ingredient:
            return ingredient
        return None

    def search_by_id(self, ID_drink):
        url = self.build_url('lookup.php?i=' + ID_drink)
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        return api_data
    def Create_Ingred(self, name: str):
        url = self.build_url('search.php?i=' + name)
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        ingredient_data = api_data['ingredients'][0]
        ingredient = Ingredient(
            name=ingredient_data['strIngredient'],
            description=ingredient_data['strDescription'],
            image=f'https://www.thecocktaildb.com/images/ingredients/{ingredient_data['strIngredient']}-Medium.png'
        )
        ingredient.save()
        return ingredient

    def Create_CockIngred(self, Cocktails, Ingredient, Measure):
        cocktail_ingredient = CocktailIngredient(
            cocktail=Cocktails,
            ingredient=Ingredient,
            measure=Measure
        )
        cocktail_ingredient.save()

    def Create_Tags(self, tags, cocktail):
        if tags:
            for tag_name in tags.split(','):
                tag_exist = Tag.objects.filter(name__exact=tag_name.strip())
                if not tag_exist:
                    tag = Tag(name=tag_name.strip())
                    tag.save()
                else:
                    tag = tag_exist.first()
                cocktail.tags.add(tag)
    # @ensure_csrf_cookie
    # @csrf_protect
    # @require_POST
    # def handle_cocktail_search(self, request):
    #     if request.method == 'POST':
    #         # Ensure that the CSRF token is present and valid
    #         if not request.META.get("HTTP_X_CSRFTOKEN"):
    #             return JsonResponse({'error': 'CSRF token missing or invalid'},
    #                                 status=403)
    #
    #         try:
    #             data = json.loads(request.body)
    #             selected_ingredients = data.get('ingredients', [])
    #
    #             # Perform your search in the database
    #             database_results = self.search_in_database(selected_ingredients)
    #
    #             # If there are results from the database, return them
    #             if database_results:
    #                 response_data = {'source': 'database',
    #                                  'results': database_results}
    #                 return JsonResponse(response_data)
    #
    #             # If no results in the database, perform a search using an external API
    #             api_results = search_in_external_api(selected_ingredients)
    #
    #             # Return the results from the external API
    #             response_data = {'source': 'api', 'results': api_results}
    #             return JsonResponse(response_data)
    #         except json.JSONDecodeError as e:
    #             return JsonResponse({'error': 'Invalid JSON format'},
    #                                 status=400)
    #
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)

    def search_in_database(self, selected_ingredients):
        # Implement your database search logic here
        # This is a placeholder; replace it with your actual database query
        selected_ingredient = Ingredient.objects.filter(name__in=selected_ingredients)
        cocktails = Cocktail.objects.filter(cocktailsingredient__ingredient__in=selected_ingredient)
        return cocktails

    def search_in_external_api(self, selected_ingredients):
        # Implement your external API search logic here
        # This is a placeholder; replace it with your actual API request
        # and processing logic
        selected_ingredients = [str(conv) for conv in selected_ingredients]
        api_params = ','.join(selected_ingredients)
        url = self.build_url('filter.php?i=' + api_params)
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        if api_data['drink'] is None:
            return None

        for drink in api_data['drink']:
            cocktail = self.dupicate_check(drink['strDrink'])
            if cocktail:
                continue
            else:
                data = self.search_by_id(drink['idDrink'])
                self.Create_Cocktails(data)

    def date_modified(self, date_modified_str):
        if date_modified_str:
            date_modified = datetime.strptime(date_modified_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        else:
            date_modified = None
        return date_modified

    def Create_Cocktails(self, JsonData):
        cocktail = Cocktail(
            name=JsonData['strDrink'],
            alternate_name=JsonData['strDrinkAlternate'],
            cocktail_tag='o',
            category=JsonData['strCategory'],
            glass=JsonData['strGlass'],
            instructions=JsonData['strInstructions'],
            image=JsonData['strDrinkThumb'],
            image_source=JsonData['strImageSource'],
            image_attribution=JsonData['strImageAttribution'],
            date_modified=self.date_modified(JsonData['dateModified'])
        )
        self.Create_Tags(JsonData['strTags'], cocktail)
        for i in range(1, 16):
            ingredient_name = JsonData['strIngredient' + str(i)]
            if ingredient_name is None:
                break
            ingredient = self.ingred_dupicated(ingredient_name)
            measure = JsonData['strMeasure' + str(i)]
            if isinstance(ingredient, Ingredient):
                self.Create_CockIngred(cocktail, ingredient, measure)
            else:
                self.Create_CockIngred(cocktail, self.Create_Ingred(ingredient_name),
                                  measure)
        cocktail.save()




# class CocktailApi:
#     def __init__(self):
#         self.base_url = config("API_KEY", default="https://www.thecocktaildb.com/api/json/v1/1/")
#
#     def build_url(self, endpoint):
#         return self.base_url + endpoint
#
#     def get_cocktail_by_name(self, name):
#         url = self.build_url('search.php?s=' + name)
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             response_data = response.json()
#         except requests.exceptions.RequestException as e:
#             print(f'Error: {e}')
#             return None
#
#         if response_data['drinks'] is None:
#             return None
#
#         cocktails_list = []
#         for i in range(len(response_data['drinks'])):
#             cocktails_data = response_data['drinks'][i]
#
#             tags_list = []
#             if cocktails_data['strTags']:
#                 for tag_name in cocktails_data['strTags'].split(','):
#                     tag_exist = Tag.objects.filter(name__exact=tag_name.strip())
#                     if not tag_exist:
#                         tag = Tag(name=tag_name.strip())
#                         tag.save()
#                     else:
#                         tag = tag_exist.first()
#                     tags_list.append(tag)
#
#             ingredients_list = []
#             if cocktails_data['strIngredient1'] is not None:
#                 for i in range(1, 16):
#                     ingredient_name = cocktails_data['strIngredient' + str(i)]
#                     measure = cocktails_data['strMeasure' + str(i)]
#                     if ingredient_name is None:
#                         break
#                     ingredient_exist = Ingredient.objects.filter(name__exact=ingredient_name)
#
#                     url_ingre = self.build_url('search.php?i=' + ingredient_name)
#                     try:
#                         response_ingre = requests.get(url_ingre)
#                         response_ingre.raise_for_status()
#                         response_ingre_data = response_ingre.json()
#                     except requests.exceptions.RequestException as e:
#                         print(f'Error: {e}')
#                         return None
#
#                     ingredient_data = response_ingre_data['ingredients'][0]
#                     if not ingredient_exist and Cocktail.ingredients.through.objects.filter(ingredient__name__exact=ingredient_name).count() == 0:
#                         ingredient = Ingredient(
#                             name = ingredient_data['strIngredient'],
#                             description = ingredient_data['strDescription'],
#                             image = f'https://www.thecocktaildb.com/images/ingredients/{ingredient_name}-Medium.png'
#                         )
#                         ingredient.save()
#                     else:
#                         ingredient = ingredient_exist.first()
#                         if 'strDescription' in ingredient_data and ingredient.description is None:
#                             ingredient.description = ingredient_data['strDescription']
#                         if ingredient.image is None:
#                             ingredient.image = f'www.thecocktaildb.com/images/ingredients/{ingredient_name}-Medium.png'
#                         ingredient.save()
#                     ingredients_list.append({
#                         'ingredient': ingredient,
#                         'measure': measure
#                     })
#
#             date_modified_str = cocktails_data['dateModified']
#             if date_modified_str:
#                 date_modified = datetime.strptime(date_modified_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
#             else:
#                 date_modified = None
#
#             cocktail_name = cocktails_data['strDrink']
#             name_exist = Cocktail.objects.filter(name__exact=cocktail_name)
#             if not name_exist:
#                 cocktail = Cocktail(
#                     name = cocktails_data['strDrink'],
#                     alternate_name = cocktails_data['strDrinkAlternate'],
#                     cocktail_tag = 'o',
#                     category = cocktails_data['strCategory'],
#                     glass = cocktails_data['strGlass'],
#                     instructions = cocktails_data['strInstructions'],
#                     image = cocktails_data['strDrinkThumb'],
#                     image_source = cocktails_data['strImageSource'],
#                     image_attribution = cocktails_data['strImageAttribution'],
#                     date_modified = date_modified
#                 )
#                 cocktail.save()
#                 for tag in tags_list:
#                     cocktail.tags.add(tag)
#                 for ingredient in ingredients_list:
#                     cocktail_ingredient = CocktailIngredient(
#                         cocktail=cocktail,
#                         ingredient=ingredient['ingredient'],
#                         measure=ingredient['measure']
#                     )
#                     cocktail_ingredient.save()
#             else:
#                 cocktail = name_exist.first()
#             cocktails_list.append(cocktail)
#         return cocktails_list
#
#     def get_ingredient_by_name(self, name):
#         ingredient_exist = Ingredient.objects.filter(name__exact=name)
#         if ingredient_exist:
#             return ingredient_exist.first()
#         url_ingre = self.build_url('search.php?i=' + name)
#         try:
#             response_ingre = requests.get(url_ingre)
#             response_ingre.raise_for_status()
#             response_ingre_data = response_ingre.json()
#         except requests.exceptions.RequestException as e:
#             print(f'Error: {e}')
#             return None
#
#         ingredient_data = response_ingre_data['ingredients'][0]
#
#         if Ingredient.objects.filter(name__exact=ingredient_data['strIngredient']):
#             return Ingredient.objects.get(name__exact=ingredient_data['strIngredient']).first()
#
#         ingredient = Ingredient.objects.create(
#             name = ingredient_data['strIngredient'],
#             description = ingredient_data['strDescription'],
#             image = f'https://www.thecocktaildb.com/images/ingredients/{name}-Medium.png'
#         )
#
#         ingredient.save()
#         return ingredient
