"""Tests of the course booking view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Student, Course

class CourseBookingViewTestCase(TestCase):
    """Tests of the course booking view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.student_user = User.objects.get(username='@johndoe')
        self.url = reverse('course_booking')

    def test_course_booking_url(self):
        self.assertEqual(self.url, '/course_booking/')

    def test_get_course_booking_as_student(self):
        self.client.login(username=self.student_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_booking.html')
        self.assertIn('available_courses', response.context)

    def test_course_booking_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
