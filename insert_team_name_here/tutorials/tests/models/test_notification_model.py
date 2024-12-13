from django.test import TestCase
from tutorials.models import Notification, User

class NotificationModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='janedoe',
            email='janedoe@example.com',
            password='password123'
        )
        # Create a notification for the user
        self.notification = Notification.objects.create(
            user=self.user,
            message="This is a test notification.",
            is_read=False
        )

    def test_notification_string_representation(self):
        """Test the string representation of a notification."""
        truncated_message = "This is a test notif..."
        expected_str = f"Notification for {self.user.username}: {truncated_message}"
        self.assertEqual(str(self.notification), expected_str)

    def test_mark_as_read(self):
        """Test the mark_as_read method."""
        self.assertFalse(self.notification.is_read)
        self.notification.mark_as_read()
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
