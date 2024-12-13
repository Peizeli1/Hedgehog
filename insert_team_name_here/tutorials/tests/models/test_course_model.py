from django.test import TestCase
from tutorials.models import Course, CourseType, Tutor

class CourseModelTestCase(TestCase):
    """Unit tests for the Course model."""

    fixtures = ['mock_data.json']

    def setUp(self):
        self.course_type = CourseType.objects.get(name='Python Basics')
        self.tutor = Tutor.objects.get(user__username='@johndoe')
        self.course = Course.objects.create(
            course_type=self.course_type,
            tutor=self.tutor,
            day_of_week='Monday',
            time_slot='10:00:00',
            duration=60,
            location='Room 101',
            status='Scheduled'
        )

    def test_course_creation(self):
        """Test that a course is created successfully."""
        self.assertIsInstance(self.course, Course)
        self.assertEqual(self.course.course_type, self.course_type)
        self.assertEqual(self.course.tutor, self.tutor)

    def test_course_string_representation(self):
        """Test the string representation of a course."""
        expected_str = f"{self.course.course_type.name} ({self.course.day_of_week})"
        self.assertEqual(str(self.course), expected_str)