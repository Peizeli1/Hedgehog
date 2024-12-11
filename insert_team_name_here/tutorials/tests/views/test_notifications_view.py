"""Tests of the notifications view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Notification

class NotificationsViewTestCase(TestCase):
    """Tests of the notifications view."""

    fixtures = ['tutorials/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('notifications')

    def test_get_notifications_as_authenticated_user(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_notifications_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
