from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from SIP.models import Official, Unofficial


class OfficialModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.official = Official.objects.create(
            id_drink=1,
            drink_name='Mojito',
            tags=['testtag'],
            glass='testglass',
            instructions='testinstructions',
            ingredients={
                'testingredient1': 'testmeasure1',
                'testingredient2': 'testmeasure2'
            },
            date_modified=datetime(2023, 11, 7, tzinfo=timezone.utc)
        )
    
    def test_official_model_created(self):
        self.assertTrue(isinstance(self.official, Official))
        self.assertEqual(str(self.official), 'Mojito')
    
    def test_official_model_fields(self):
        self.assertEqual(self.official.id_drink, 1)
        self.assertEqual(self.official.drink_name, 'Mojito')
        self.assertEqual(self.official.tags, ['testtag'])
        self.assertEqual(self.official.glass, 'testglass')
        self.assertEqual(self.official.instructions, 'testinstructions')
        self.assertEqual(self.official.ingredients, {
            'testingredient1': 'testmeasure1',
            'testingredient2': 'testmeasure2'
        })
        self.assertEqual(self.official.date_modified, datetime(2023, 11, 7, tzinfo=timezone.utc))


class UnofficialModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.unofficial = Unofficial.objects.create(
            drink_name='Jojito',
            tags=['testtag'],
            glass='testglass',
            instructions='testinstructions',
            ingredients={
                'testingredient1': 'testmeasure1',
                'testingredient2': 'testmeasure2',
                'testingredient3': 'testmeasure3'
            },
            date_modified=datetime(2023, 11, 7, tzinfo=timezone.utc)
        )
    
    def test_unofficial_model_created(self):
        self.assertTrue(isinstance(self.unofficial, Unofficial))
        self.assertEqual(str(self.unofficial), 'Jojito')
    
    def test_unofficial_model_fields(self):
        self.assertEqual(self.unofficial.id_drink, 2)
        self.assertEqual(self.unofficial.drink_name, 'Jojito')
        self.assertEqual(self.unofficial.tags, ['testtag'])
        self.assertEqual(self.unofficial.glass, 'testglass')
        self.assertEqual(self.unofficial.instructions, 'testinstructions')
        self.assertEqual(self.unofficial.ingredients, {
            'testingredient1': 'testmeasure1',
            'testingredient2': 'testmeasure2',
            'testingredient3': 'testmeasure3'
        })
        self.assertEqual(self.unofficial.date_modified, datetime(2023, 11, 7, tzinfo=timezone.utc))
