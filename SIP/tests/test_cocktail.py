from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from SIP.models import Tag, Ingredient, CocktailIngredient, Cocktail


class CocktailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.tag1 = Tag.objects.create(
            name='testtag1',
        )
        self.tag2 = Tag.objects.create(
            name='testtag2',
        )

        self.ingredient1 = Ingredient.objects.create(
            name='testingredient1',
            description='testdescription1',
        )
        self.ingredient2 = Ingredient.objects.create(
            name='testingredient2',
            description='testdescription2',
        )

        self.cocktail = Cocktail.objects.create(
            name='testcocktail',
            alternate_name='testalternatename',
            cocktail_tag='o',
            category='testcategory',
            glass='testglass',
            instructions='testinstructions',
            date_modified=datetime(2023, 11, 7, tzinfo=timezone.utc)
        )

        self.cocktail.tags.add(self.tag1)
        self.cocktail.tags.add(self.tag2)

        CocktailIngredient.objects.create(
            cocktail=self.cocktail,
            ingredient=self.ingredient1,
            measure='testmeasure1'
        )

        CocktailIngredient.objects.create(
            cocktail=self.cocktail,
            ingredient=self.ingredient2,
            measure='testmeasure2'
        )
    
    def test_cocktail_model_created(self):
        self.assertTrue(isinstance(self.cocktail, Cocktail))
        self.assertEqual(str(self.cocktail), 'testcocktail')

    def test_cocktail_name(self):
        self.assertEqual(self.cocktail.name, 'testcocktail')

    def test_cocktail_cocktail_tag(self):
        self.assertEqual(self.cocktail.cocktail_tag, 'o')
    
    def test_cocktail_category(self):
        self.assertEqual(self.cocktail.category, 'testcategory')

    def test_cocktail_glass(self):
        self.assertEqual(self.cocktail.glass, 'testglass')

    def test_cocktail_instructions(self):
        self.assertEqual(self.cocktail.instructions, 'testinstructions')

    def test_cocktail_date_modified(self):
        self.assertEqual(self.cocktail.date_modified, datetime(2023, 11, 7, tzinfo=timezone.utc))

    def test_cocktail_with_ingredients(self):
        cocktail_ingredients = self.cocktail.cocktailingredient_set.all()
        self.assertEqual(len(cocktail_ingredients), 2)
        list_ingredients = ['testingredient1', 'testingredient2']
        for ingredient in cocktail_ingredients:
            self.assertIn(str(ingredient).split(' ')[1], list_ingredients)

    def test_cocktail_with_tags(self):
        tags = self.cocktail.tags.all()
        self.assertEqual(len(tags), 2)
        list_tags = ['testtag1', 'testtag2']
        for tag in tags:
            self.assertIn(tag.name, list_tags)
