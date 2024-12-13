from django.test import TestCase
from tutorials.forms import PasswordForm

class PasswordFormTestCase(TestCase):
    """Unit tests for the PasswordForm."""

    def setUp(self):
        self.form_input = {
            'password': 'Password123!',
            'confirm_password': 'Password123!',
        }

    def test_form_has_necessary_fields(self):
        """Test that the form has the necessary fields."""
        form = PasswordForm()
        self.assertIn('password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    def test_valid_form(self):
        """Test that the form is valid when passwords match."""
        form = PasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_passwords_do_not_match(self):
        """Test that the form is invalid when passwords do not match."""
        self.form_input['confirm_password'] = 'DifferentPassword123!'
        form = PasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)