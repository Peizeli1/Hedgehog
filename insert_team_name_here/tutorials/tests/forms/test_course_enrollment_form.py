from django.test import TestCase
from tutorials.forms import CourseEnrollmentForm
from tutorials.models import Student, Course, CourseEnrollment

class CourseEnrollmentFormTestCase(TestCase):
    """Unit tests for the CourseEnrollmentForm."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.student = Student.objects.get(user__username='@petrapickles')
        self.course = Course.objects.get(course_type__name='Python Basics')
        self.form_input = {
            'student': self.student.id,
            'course': self.course.id,
        }

    def test_form_has_necessary_fields(self):
        """Test that the form has the necessary fields."""
        form = CourseEnrollmentForm()
        self.assertIn('student', form.fields)
        self.assertIn('course', form.fields)

    def test_valid_form(self):
        """Test that the form is valid when given correct input."""
        form = CourseEnrollmentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_duplicate_enrollment_is_invalid(self):
        """Test that a duplicate enrollment is considered invalid."""
        CourseEnrollment.objects.create(student=self.student, course=self.course)
        form = CourseEnrollmentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)
_