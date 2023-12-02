from django.test import TestCase
from SIP.models import Cocktail
from SIP.views import CocktailApi


class CocktailApiTest(TestCase):
    def test_get_search_by_name(self):
        cocktail_api = CocktailApi()
        cocktails_list = cocktail_api.get_search_by_name('Mojito')
        if cocktails_list is not None:
            self.assertIsInstance(cocktails_list, list)
        if cocktails_list != [] and not None:
            first_cocktail = cocktails_list[0]
            self.assertIsInstance(first_cocktail, Cocktail)
            
            self.assertEqual(first_cocktail.name, 'Mojito')

    def test_get_search_by_name_not_found(self):
        cocktail_api = CocktailApi()
        cocktails_list = cocktail_api.get_search_by_name('NonExistentCocktail')
        self.assertIsNone(cocktails_list)
