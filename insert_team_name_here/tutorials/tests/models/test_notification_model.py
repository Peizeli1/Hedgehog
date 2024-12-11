from django.test import TestCase
from tutorials.models import User, Notification

class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    fixtures = ['default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.notification = Notification.objects.create(
            user=self.user,
            message='Test Notification',
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, 'Test Notification')
        self.assertFalse(self.notification.is_read)

    def test_str_representation(self):
        self.assertEqual(str(self.notification), 'Notification for @johndoe: Test Notification')
