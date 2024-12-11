from django.contrib.auth.hashers import check_password
from django.test import TestCase
from tutorials.models import User
from tutorials.forms import PasswordForm

class PasswordFormTestCase(TestCase):
    fixtures = ['default_user.json', 'other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@janedoe')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    def test_form_has_necessary_fields(self):
        form = PasswordForm(user=self.user)
        self.assertIn('password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    def test_valid_form(self):
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertTrue(form.is_valid())
