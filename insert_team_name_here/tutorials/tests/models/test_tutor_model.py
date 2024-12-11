from django.test import TestCase
from tutorials.models import User, Tutor

class TutorModelTestCase(TestCase):
    """Unit tests for the Tutor model."""

    fixtures = ['default_data.json']

    def setUp(self):
        self.user = User.objects.get(username='@tutor1')
        self.tutor = Tutor.objects.create(
            user=self.user,
            expertise="Python, Django",
            is_available=True
        )

    def test_tutor_creation(self):
        self.assertEqual(self.tutor.user, self.user)
        self.assertEqual(self.tutor.expertise, "Python, Django")
        self.assertTrue(self.tutor.is_available)

    def test_str_representation(self):
        self.assertEqual(str(self.tutor), f"Tutor: {self.user.full_name()}")
