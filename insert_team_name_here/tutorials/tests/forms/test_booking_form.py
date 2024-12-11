from django.test import TestCase
from tutorials.forms import BookingForm
from tutorials.models import Student, Course, Booking

class BookingFormTestCase(TestCase):
    """Unit tests for the BookingForm."""

    fixtures = ['default_user.json', 'other_users.json', 'default_data.json']

    def setUp(self):
        self.student = Student.objects.get(user__username='@janedoe')
        self.course = Course.objects.get(course_type__name='Python Basics')
        self.form_input = {
            'student': self.student.id,
            'course': self.course.id,
        }

    def test_form_has_necessary_fields(self):
        form = BookingForm()
        self.assertIn('student', form.fields)
        self.assertIn('course', form.fields)

    def test_valid_form(self):
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_duplicate_booking_is_invalid(self):
        Booking.objects.create(student=self.student, course=self.course)
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)
