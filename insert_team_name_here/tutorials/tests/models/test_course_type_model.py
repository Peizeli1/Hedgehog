from django.test import TestCase
from tutorials.models import CourseType

class CourseTypeModelTestCase(TestCase):
    """Unit tests for the CourseType model."""

    def setUp(self):
        self.course_type = CourseType.objects.create(
            name="Python Basics",
            description="An introduction to Python programming.",
            skill_level="Beginner"
        )

    def test_course_type_creation(self):
        self.assertEqual(self.course_type.name, "Python Basics")
        self.assertEqual(self.course_type.description, "An introduction to Python programming.")
        self.assertEqual(self.course_type.skill_level, "Beginner")

    def test_str_representation(self):
        self.assertEqual(str(self.course_type), "Python Basics")
