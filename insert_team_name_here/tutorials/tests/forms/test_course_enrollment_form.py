from django.test import TestCase
from tutorials.forms import CourseEnrollmentForm
from tutorials.models import Student, Course

class CourseEnrollmentFormTestCase(TestCase):
    """Unit tests for the CourseEnrollmentForm."""

    fixtures = ['default_user.json', 'other_users.json', 'default_data.json']

    def setUp(self):
        self.student = Student.objects.get(user__username='@janedoe')
        self.course = Course.objects.get(course_type__name='Python Basics')
        self.form_input = {
            'student': self.student.id,
            'course': self.course.id,
        }

    def test_form_has_necessary_fields(self):
        form = CourseEnrollmentForm()
        self.assertIn('student', form.fields)
        self.assertIn('course', form.fields)

    def test_valid_form(self):
        form = CourseEnrollmentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_student_field(self):
        self.form_input['student'] = -1  # Invalid student ID
        form = CourseEnrollmentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_course_field(self):
        self.form_input['course'] = -1  # Invalid course ID
        form = CourseEnrollmentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
