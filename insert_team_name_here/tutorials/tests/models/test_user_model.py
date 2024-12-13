from django.test import TestCase
from tutorials.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.user = User.objects.get(username='@janedoe')

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, '@janedoe')
        self.assertEqual(self.user.email, 'janedoe@example.org')

    def test_user_string_representation(self):
        """Test the string representation of a user."""
        expected_str = f"{self.user.first_name} {self.user.last_name} (@{self.user.username}) - {self.user.role.capitalize()}"
        self.assertEqual(str(self.user), expected_str)