from django.test import TestCase
from tutorials.forms import LogInForm

class LogInFormTestCase(TestCase):
    """Unit tests for the LogInForm."""

    def setUp(self):
        self.form_input = {
            'username': 'testuser',
            'password': 'Password123!',
        }

    def test_form_has_necessary_fields(self):
        """Test that the form has the necessary fields."""
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

    def test_valid_form(self):
        """Test that the form is valid when given correct input."""
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        """Test that the form is invalid when the username is missing."""
        self.form_input.pop('username')
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_form_missing_password(self):
        """Test that the form is invalid when the password is missing."""
        self.form_input.pop('password')
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)