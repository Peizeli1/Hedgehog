from django.test import TestCase
from tutorials.forms import StudentBookingForm
from tutorials.models import Student, Course, Booking

class StudentBookingFormTestCase(TestCase):
    """Unit tests for the StudentBookingForm."""

    fixtures = ['tutorials/tests/fixtures/default_data.json']  # Update with appropriate fixtures

    def setUp(self):
        self.student = Student.objects.get(username='@student1')
        self.course = Course.objects.get(name='Sample Course')
        self.form_input = {
            'student': self.student.id,
            'course': self.course.id,
        }

    def test_form_has_necessary_fields(self):
        form = StudentBookingForm()
        self.assertIn('student', form.fields)
        self.assertIn('course', form.fields)

    def test_valid_form(self):
        form = StudentBookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_student_field_is_readonly(self):
        form = StudentBookingForm()
        self.assertIn('readonly', form.fields['student'].widget.attrs)

    def test_duplicate_booking_is_invalid(self):
        Booking.objects.create(student=self.student, course=self.course)
        form = StudentBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)
