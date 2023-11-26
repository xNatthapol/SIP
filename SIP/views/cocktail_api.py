import requests
from datetime import datetime
from django.utils import timezone
from SIP.models import Tag, Ingredient, CocktailIngredient, Cocktail
from decouple import config


class CocktailApi:
    def __init__(self):
        self.base_url = config("API_KEY", default="https://www.thecocktaildb.com/api/json/v1/1/")

    def build_url(self, endpoint):
        return self.base_url + endpoint
    
    # def change_none_measure(self, measure):
    #     """If the measure unit of that ingredient is None, return 'Varies'."""
    #     if measure is None:
    #         return 'Varies'
    #     return measure

    def get_cocktail_by_name(self, name):
        url = self.build_url('search.php?s=' + name)
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None

        if response_data['drinks'] is None:
            return None

        cocktails_list = []
        for i in range(len(response_data['drinks'])):
            cocktails_data = response_data['drinks'][i]

            tags_list = []
            if cocktails_data['strTags']:
                for tag_name in cocktails_data['strTags'].split(','):
                    tag_exist = Tag.objects.filter(name__exact=tag_name.strip())
                    if not tag_exist:
                        tag = Tag(name=tag_name.strip())
                        tag.save()
                    else:
                        tag = tag_exist.first()
                    tags_list.append(tag)

            ingredients_list = []
            if cocktails_data['strIngredient1'] is not None:
                for i in range(1, 16):
                    ingredient_name = cocktails_data['strIngredient' + str(i)]
                    measure = cocktails_data['strMeasure' + str(i)]
                    if ingredient_name is None:
                        break
                    
                    # measure = self.change_none_measure(measure)

                    ingredient_exist = Ingredient.objects.filter(name__exact=ingredient_name)

                    url_ingre = self.build_url('search.php?i=' + ingredient_name)
                    try:
                        response_ingre = requests.get(url_ingre)
                        response_ingre.raise_for_status()
                        response_ingre_data = response_ingre.json()
                    except requests.exceptions.RequestException as e:
                        print(f'Error: {e}')
                        return None

                    ingredient_data = response_ingre_data['ingredients'][0]
                    if not ingredient_exist and Cocktail.ingredients.through.objects.filter(ingredient__name__exact=ingredient_name).count() == 0:
                        ingredient = Ingredient(
                            name = ingredient_data['strIngredient'],
                            description = ingredient_data['strDescription'],
                            image = f'https://www.thecocktaildb.com/images/ingredients/{ingredient_name}-Medium.png'
                        )
                        ingredient.save()
                    else:
                        ingredient = ingredient_exist.first()
                        if 'strDescription' in ingredient_data and ingredient.description is None:
                            ingredient.description = ingredient_data['strDescription']
                        if ingredient.image is None:
                            ingredient.image = f'www.thecocktaildb.com/images/ingredients/{ingredient_name}-Medium.png'
                        ingredient.save()
                    ingredients_list.append({
                        'ingredient': ingredient,
                        'measure': measure
                    })
            
            date_modified_str = cocktails_data['dateModified']
            if date_modified_str:
                date_modified = datetime.strptime(date_modified_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            else:
                date_modified = None
                
            cocktail_name = cocktails_data['strDrink']
            name_exist = Cocktail.objects.filter(name__exact=cocktail_name)
            if not name_exist:
                cocktail = Cocktail(
                    name = cocktails_data['strDrink'],
                    alternate_name = cocktails_data['strDrinkAlternate'],
                    cocktail_tag = 'o',
                    category = cocktails_data['strCategory'],
                    glass = cocktails_data['strGlass'],
                    instructions = cocktails_data['strInstructions'],
                    image = cocktails_data['strDrinkThumb'],
                    image_source = cocktails_data['strImageSource'],
                    image_attribution = cocktails_data['strImageAttribution'],
                    date_modified = date_modified
                )
                cocktail.save()
                for tag in tags_list:
                    cocktail.tags.add(tag)
                for ingredient in ingredients_list:
                    cocktail_ingredient = CocktailIngredient(
                        cocktail=cocktail,
                        ingredient=ingredient['ingredient'],
                        measure=ingredient['measure']
                    )
                    cocktail_ingredient.save()
            else:
                cocktail = name_exist.first()
            cocktails_list.append(cocktail)
        return cocktails_list

    def get_ingredient_by_name(self, name):
        ingredient_exist = Ingredient.objects.filter(name__exact=name)
        if ingredient_exist:
            return ingredient_exist.first()
        url_ingre = self.build_url('search.php?i=' + name)
        try:
            response_ingre = requests.get(url_ingre)
            response_ingre.raise_for_status()
            response_ingre_data = response_ingre.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None

        ingredient_data = response_ingre_data['ingredients'][0]

        if Ingredient.objects.filter(name__exact=ingredient_data['strIngredient']):
            return Ingredient.objects.get(name__exact=ingredient_data['strIngredient']).first()

        ingredient = Ingredient.objects.create(
            name = ingredient_data['strIngredient'],
            description = ingredient_data['strDescription'],
            image = f'https://www.thecocktaildb.com/images/ingredients/{name}-Medium.png'
        )

        ingredient.save()
        return ingredient
