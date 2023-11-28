import json
from itertools import chain

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
        self.base_url = config("API_KEY",
                               default="https://www.thecocktaildb.com/api/json/v1/1/")

    def build_url(self, endpoint):
        return self.base_url + endpoint

    @staticmethod
    def dupicate_check(drink_name):
        cocktail = Cocktail.objects.filter(name__exact=drink_name,
                                           cocktail_tag__exact='o')
        if cocktail:
            return cocktail
        return None

    @staticmethod
    def ingred_dupicated(ingerd_name):
        ingredient = Ingredient.objects.filter(name__exact=ingerd_name)
        if ingredient:
            return ingredient
        return None

    @staticmethod
    def database_search_by_ingredient(selected_ingredients):
        # This is a placeholder; replace it with your actual database query
        selected_ingredient = Ingredient.objects.filter(
            name__in=selected_ingredients)
        cocktails = Cocktail.objects.filter(
            cocktailingredient__ingredient__in=selected_ingredient,
            cocktail_tag__exact='u'
        )
        if not cocktails:
            return []
        if cocktails and len(cocktails) > 1:
            cocktails = list(chain(*cocktails))
        else:
            cocktails = cocktails[0]
        return cocktails

    @staticmethod
    def database_search_by_name(name):
        cocktails = Cocktail.objects.filter(name__in=name,
                                            cocktail_tag__exact='u')
        return cocktails

    @staticmethod
    def create_cock_ingred(cocktails, ingredient, measure):
        cocktail_ingredient = CocktailIngredient(
            cocktail=cocktails,
            ingredient=ingredient,
            measure=measure
        )
        cocktail_ingredient.save()

    @staticmethod
    def create_tags(tags, cocktail):
        if tags:
            for tag_name in tags.split(','):
                tag_exist = Tag.objects.filter(name__exact=tag_name.strip())
                if not tag_exist:
                    tag = Tag(name=tag_name.strip())
                    tag.save()
                else:
                    tag = tag_exist.first()
                cocktail.tags.add(tag)
            cocktail.save()

    @staticmethod
    def date_modified(date_modified_str):
        if date_modified_str:
            date_modified = datetime.strptime(date_modified_str,
                                              '%Y-%m-%d %H:%M:%S').replace(
                tzinfo=timezone.utc)
        else:
            date_modified = None
        return date_modified

    def get_cocktails_endpoint(self, url):
        cocktails = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        if api_data['drinks'] is None or api_data['drinks'] == "None Found":
            return None
        for drink in api_data['drinks']:
            cocktail = self.dupicate_check(drink['strDrink'])
            if not cocktail:
                data = self.search_by_id(drink['idDrink'])['drinks'][0]
                cocktail = self.create_cocktails(data)
            else:
                cocktail = cocktail.first()
            cocktails.append(cocktail)
        return cocktails

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

    def create_ingred(self, name: str):
        url = self.build_url('search.php?i=' + name)
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        ingredient_data = api_data['ingredients'][0]
        name = ingredient_data['strIngredient']
        ingredient = Ingredient(
            name=ingredient_data['strIngredient'],
            description=ingredient_data['strDescription'],
            image=f'https://www.thecocktaildb.com/images/ingredients/{name}-Medium.png'
        )
        ingredient.save()
        return ingredient

    def api_search_by_ingredient(self, selected_ingredients):

        selected_ingredients = [str(conv).strip().replace(" ","_") for conv in selected_ingredients]
        api_params = ','.join(selected_ingredients)
        url = self.build_url('filter.php?i=' + api_params)
        return self.get_cocktails_endpoint(url)

    def create_cocktails(self, JsonData):
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
        cocktail.save()
        self.create_tags(JsonData['strTags'], cocktail)
        for i in range(1, 16):
            ingredient_name = JsonData['strIngredient' + str(i)]
            if ingredient_name is None:
                break
            ingredient = self.ingred_dupicated(ingredient_name)
            measure = JsonData['strMeasure' + str(i)]
            if isinstance(ingredient, Ingredient):
                self.create_cock_ingred(cocktail, ingredient, measure)
            else:
                self.create_cock_ingred(cocktail,
                                        self.create_ingred(ingredient_name),
                                        measure)

        return cocktail

    def api_search_by_name(self, name):
        url = self.build_url('search.php?s=' + name)
        return self.get_cocktails_endpoint(url)
