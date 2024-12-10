from django.test import TestCase
from tutorials.models import User, Notification

class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@janedoe',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.com',
            password='Password123'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message="This is a test notification."
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, "This is a test notification.")
        self.assertFalse(self.notification.is_read)

    def test_mark_as_read(self):
        self.notification.mark_as_read()
        self.assertTrue(self.notification.is_read)

    def test_str_representation(self):
        self.assertEqual(
            str(self.notification),
            "Notification for @janedoe: This is a test notifica..."
        )
