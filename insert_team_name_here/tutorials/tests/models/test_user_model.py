from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = ['default_user.json', 'other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_must_be_unique(self):
        duplicate_user = User.objects.get(username='@janedoe')
        self.user.username = duplicate_user.username
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
