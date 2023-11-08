from django.test import TestCase
from SIP.models import Official
from SIP.views import CocktailApi

class CocktailApiTestCase(TestCase):
    def test_get_cocktail_by_name(self):
        cocktail_api = CocktailApi()
        cocktails_list = cocktail_api.get_cocktail_by_name('Mojito')
        self.assertIsInstance(cocktails_list, list)
        if cocktails_list != []:
            first_cocktail = cocktails_list[0]
            self.assertIsInstance(first_cocktail, Official)
            
            self.assertEqual(first_cocktail.drink_name, 'Mojito')

    def test_get_cocktail_by_name_not_found(self):
        cocktail_api = CocktailApi()
        cocktails_list = cocktail_api.get_cocktail_by_name('NonExistentCocktail')
        self.assertIsNone(cocktails_list)
