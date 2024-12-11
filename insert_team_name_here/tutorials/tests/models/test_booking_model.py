from django.test import TestCase
from tutorials.models import Student, Course, Booking

class BookingModelTestCase(TestCase):
    """Unit tests for the Booking model."""

    fixtures = ['default_data.json']

    def setUp(self):
        self.student = Student.objects.get(user__username='@student1')
        self.course = Course.objects.get(name='Sample Course')

    def test_booking_creation(self):
        booking = Booking.objects.create(student=self.student, course=self.course)
        self.assertEqual(booking.student, self.student)
        self.assertEqual(booking.course, self.course)

    def test_str_representation(self):
        booking = Booking.objects.create(student=self.student, course=self.course)
        self.assertEqual(str(booking), f"{self.student.user.username} - {self.course.name}")
