from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from SIP.models import Cocktail, Review, Star


class ReviewModelTest(TestCase):
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

        self.review = Review.objects.create(
            cocktail=self.cocktail,
            user=self.user,
            message='testmessage'
        )

    def test_review_model_created(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(str(self.review), 'testmessage')

    def test_review_model_fields(self):
        self.assertEqual(self.review.cocktail, self.cocktail)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.message, 'testmessage')


class StarModelTest(TestCase):
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

        self.star = Star.objects.create(
            cocktail=self.cocktail,
            user=self.user,
            score=5
        )

    def test_star_model_created(self):
        self.assertTrue(isinstance(self.star, Star))
        self.assertEqual(int(str(self.star)), 5)

    def test_star_model_fields(self):
        self.assertEqual(self.star.cocktail, self.cocktail)
        self.assertEqual(self.star.user, self.user)
        self.assertEqual(self.star.score, 5)
