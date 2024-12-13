from django.test import TestCase
from tutorials.models import CourseType

class CourseTypeModelTestCase(TestCase):
    """Unit tests for the CourseType model."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.course_type = CourseType.objects.get(name='Python Basics')

    def test_course_type_creation(self):
        """Test that a course type is created successfully."""
        self.assertIsInstance(self.course_type, CourseType)
        self.assertEqual(self.course_type.name, 'Python Basics')

    def test_course_type_string_representation(self):
        """Test the string representation of a course type."""
        self.assertEqual(str(self.course_type), 'Python Basics')