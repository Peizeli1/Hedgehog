from django.test import TestCase
from tutorials.forms import UserForm
from tutorials.models import User

class UserFormTestCase(TestCase):
    """Unit tests for the UserForm."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe',
            'email': 'janedoe@example.com',
        }

    def test_form_has_necessary_fields(self):
        """Test that the form has the necessary fields."""
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)

    def test_valid_form(self):
        """Test that the form is valid when given correct input."""
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        """Test that the form is invalid when the username is missing."""
        self.form_input.pop('username')
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_form_invalid_email(self):
        """Test that the form is invalid when the email is invalid."""
        self.form_input['email'] = 'not-an-email'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)