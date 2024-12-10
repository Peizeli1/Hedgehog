from django.test import TestCase
from tutorials.models import User, Tutor, CourseType

class TutorModelTestCase(TestCase):
    """Unit tests for the Tutor model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@tutor1',
            first_name='Tutor',
            last_name='One',
            email='tutor1@example.com',
            password='Password123',
            role='tutor'
        )
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
        self.assertEqual(str(self.tutor), self.user.full_name())
