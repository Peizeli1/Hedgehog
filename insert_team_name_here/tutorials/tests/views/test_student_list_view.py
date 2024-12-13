"""Tests of the student list view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Student

class StudentListViewTestCase(TestCase):
    """Tests of the student list view."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.admin_user = User.objects.get(username='@admin')
        self.url = reverse('tutorials:student_list')

    def test_student_list_url(self):
        self.assertEqual(self.url, '/students/')

    def test_get_student_list_as_admin(self):
        self.client.login(username=self.admin_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_list.html')
        self.assertIn('students', response.context)

    def test_student_list_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = f"{reverse('tutorials:log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
