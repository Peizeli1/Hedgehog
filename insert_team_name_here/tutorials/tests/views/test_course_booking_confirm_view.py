"""Tests of the course booking confirm view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Course

class CourseBookingConfirmViewTestCase(TestCase):
    """Tests of the course booking confirm view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.student_user = User.objects.get(username='@johndoe')
        self.course = Course.objects.first()
        self.url = reverse('course_booking_confirm', kwargs={'course_id': self.course.id})

    def test_course_booking_confirm_url(self):
        self.assertEqual(self.url, f'/course_booking/{self.course.id}/confirm/')

    def test_get_course_booking_confirm_as_student(self):
        self.client.login(username=self.student_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_booking_confirm.html')
        self.assertIn('course', response.context)

    def test_course_booking_confirm_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
