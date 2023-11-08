from django.test import TestCase
from django.contrib.auth.models import User
from SIP.models import Review, Star


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.review = Review.objects.create(
            id_drink=1,
            tag='u',
            user=self.user,
            message='testmessage'
        )

    def test_review_model_created(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(str(self.review), 'testmessage')

    def test_review_model_fields(self):
        self.assertEqual(self.review.id_drink, 1)
        self.assertEqual(self.review.tag, 'u')
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.message, 'testmessage')


class StarModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.star = Star.objects.create(
            id_drink=1,
            tag='o',
            user=self.user,
            score=5
        )

    def test_star_model_created(self):
        self.assertTrue(isinstance(self.star, Star))
        self.assertEqual(int(str(self.star)), 5)

    def test_star_model_fields(self):
        self.assertEqual(self.star.id_drink, 1)
        self.assertEqual(self.star.tag, 'o')
        self.assertEqual(self.star.user, self.user)
        self.assertEqual(self.star.score, 5)
