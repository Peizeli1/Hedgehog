from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Notification, CourseEnrollment

class DashboardViewTestCase(TestCase):
    """Test cases for the Dashboard view."""

    fixtures = ['tutorials/fixtures/default_data.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_dashboard_renders_correctly(self):
        response = self.client.get(reverse('tutorials:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unread_notifications_count(self):
        Notification.objects.create(user=self.user, message="Test Notification", is_read=False)
        response = self.client.get(reverse('tutorials:dashboard'))
        self.assertEqual(response.context['unread_notifications_count'], 1)
