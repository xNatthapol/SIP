from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from SIP.models import Cocktail


class CocktailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.cocktail = Cocktail.objects.create(
            name='Mojito',
            cocktail_tag='o',
            tags=['testtag'],
            glass='testglass',
            instructions='testinstructions',
            ingredients={
                'testingredient1': 'testmeasure1',
                'testingredient2': 'testmeasure2'
            },
            date_modified=datetime(2023, 11, 7, tzinfo=timezone.utc)
        )
    
    def test_cocktail_model_created(self):
        self.assertTrue(isinstance(self.cocktail, Cocktail))
        self.assertEqual(str(self.cocktail), 'Mojito')
    
    def test_cocktail_model_fields(self):
        self.assertEqual(self.cocktail.name, 'Mojito')
        self.assertEqual(self.cocktail.cocktail_tag, 'o')
        self.assertEqual(self.cocktail.tags, ['testtag'])
        self.assertEqual(self.cocktail.glass, 'testglass')
        self.assertEqual(self.cocktail.instructions, 'testinstructions')
        self.assertEqual(self.cocktail.ingredients, {
            'testingredient1': 'testmeasure1',
            'testingredient2': 'testmeasure2'
        })
        self.assertEqual(self.cocktail.date_modified, datetime(2023, 11, 7, tzinfo=timezone.utc))
