import requests
from datetime import datetime
from django.utils import timezone
from SIP.models import Cocktail


class CocktailApi:
    def __init__(self):
        self.base_url = 'https://www.thecocktaildb.com/api/json/v1/1/'

    def build_url(self, endpoint):
        return self.base_url + endpoint
    
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

            tag_list = []
            if cocktails_data['strTags']:
                for tag in cocktails_data['strTags'].split(','):
                    tag_list.append(tag.strip())

            ingredients_dict = {}
            if cocktails_data['strIngredient1'] is not None:
                for i in range(1, 16):
                    ingredient = cocktails_data['strIngredient' + str(i)]
                    if ingredient is not None:
                        ingredients_dict[ingredient] = cocktails_data['strMeasure' + str(i)]
            
            date_modified_str = cocktails_data['dateModified']
            if date_modified_str:
                date_modified = datetime.strptime(date_modified_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            else:
                date_modified = None
                
            cocktail = Cocktail(
                name = cocktails_data['strDrink'],
                alternate_name = cocktails_data['strDrinkAlternate'],
                cocktail_tag = 'o',
                tags = tag_list,
                category = cocktails_data['strCategory'],
                glass = cocktails_data['strGlass'],
                instructions = cocktails_data['strInstructions'],
                ingredients = ingredients_dict,
                image = cocktails_data['strDrinkThumb'],
                image_source = cocktails_data['strImageSource'],
                image_attribution = cocktails_data['strImageAttribution'],
                date_modified = date_modified
            )
            cocktail.save()
            cocktails_list.append(cocktail)
        return cocktails_list
