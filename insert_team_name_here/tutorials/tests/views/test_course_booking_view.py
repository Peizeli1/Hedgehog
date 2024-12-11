from django.test import TestCase
from django.urls import reverse
from tutorials.models import User, Student, Course

class CourseBookingViewTestCase(TestCase):
    """Test cases for the Course Booking view."""

    fixtures = ['tutorials/fixtures/default_data.json']

    def setUp(self):
        self.user = User.objects.get(username='@student1')
        self.client.force_login(self.user)

    def test_course_booking_view_loads(self):
        response = self.client.get(reverse('tutorials:course_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_booking.html')

    def test_course_booking_post(self):
        student = Student.objects.get(user=self.user)
        course = Course.objects.get(name='Sample Course')
        response = self.client.post(reverse('tutorials:course_booking'), {'student': student.id, 'course': course.id})
        self.assertRedirects(response, reverse('tutorials:dashboard'))
