from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tutorials.forms import SignUpForm
from tutorials.models import User

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    fixtures = ['default_user.json', 'other_users.json']

    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': '@johnsmith',
            'email': 'johnsmith@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
