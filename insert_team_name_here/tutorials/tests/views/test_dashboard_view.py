"""Tests of the dashboard view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Student, Tutor, CourseEnrollment

class DashboardViewTestCase(TestCase):
    """Tests of the dashboard view."""

    fixtures = [
        'tutorials/tests/fixtures/default_user.json',
        'tutorials/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.student_user = User.objects.get(username='@johndoe')
        self.tutor_user = User.objects.get(username='@janedoe')
        self.url = reverse('dashboard')

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard_as_student(self):
        self.client.login(username=self.student_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('unread_notifications_count', response.context)
        self.assertIn('course_count', response.context)

    def test_get_dashboard_as_tutor(self):
        self.client.login(username=self.tutor_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('courses', response.context)

    def test_dashboard_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
