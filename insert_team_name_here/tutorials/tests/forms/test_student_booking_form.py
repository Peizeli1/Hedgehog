from django.test import TestCase
from tutorials.forms import StudentBookingForm
from tutorials.models import Student, Course, Booking

class StudentBookingFormTestCase(TestCase):
    """Unit tests for the StudentBookingForm."""

    fixtures = [
        'default_user.json',
        'default_data.json'
    ]

    def setUp(self):
        # Retrieve mock student and course data from fixtures
        self.student = Student.objects.get(user__username='@janedoe')
        self.course = Course.objects.get(name='Beginner Python')
        self.form_input = {
            'student': self.student.id,
            'course': self.course.id,
        }

    def test_form_has_necessary_fields(self):
        """Ensure the form has the required fields."""
        form = StudentBookingForm()
        self.assertIn('student', form.fields)
        self.assertIn('course', form.fields)

    def test_valid_form(self):
        """Test that the form accepts valid input."""
        form = StudentBookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_student_field_is_readonly(self):
        """Check that the student field is marked as readonly."""
        form = StudentBookingForm()
        self.assertIn('readonly', form.fields['student'].widget.attrs)

    def test_duplicate_booking_is_invalid(self):
        """Test that duplicate bookings for the same student and course are invalid."""
        Booking.objects.create(student=self.student, course=self.course)
        form = StudentBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)

    def test_invalid_student_field(self):
        """Test that an invalid student ID is rejected."""
        self.form_input['student'] = -1  # Non-existent student ID
        form = StudentBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_course_field(self):
        """Test that an invalid course ID is rejected."""
        self.form_input['course'] = -1  # Non-existent course ID
        form = StudentBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        """Test that the form saves valid input correctly."""
        form = StudentBookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        booking = form.save()
        self.assertEqual(booking.student, self.student)
        self.assertEqual(booking.course, self.course)

    def test_form_does_not_save_invalid_data(self):
        """Test that invalid form data is not saved."""
        self.form_input['course'] = -1  # Invalid course ID
        form = StudentBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
