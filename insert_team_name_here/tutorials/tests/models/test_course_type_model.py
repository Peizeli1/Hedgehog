from django.test import TestCase
from tutorials.models import CourseType


class CourseTypeModelTestCase(TestCase):
    """Unit tests for the CourseType model."""

    def setUp(self):
        """Set up a CourseType instance for testing."""
        self.course_type = CourseType.objects.create(
            name="Python Basics",
            description="An introduction to Python programming.",
            skill_level="Beginner"
        )

    def test_course_type_fields(self):
        """Test that the fields of the CourseType model are correctly set."""
        self.assertEqual(self.course_type.name, "Python Basics")
        self.assertEqual(self.course_type.description, "An introduction to Python programming.")
        self.assertEqual(self.course_type.skill_level, "Beginner")

    def test_course_type_str_representation(self):
        """Test the string representation of a CourseType instance."""
        self.assertEqual(str(self.course_type), "Python Basics")

    def test_course_type_skill_level_choices(self):
        """Test that the skill_level field accepts only valid choices."""
        with self.assertRaises(ValueError):
            CourseType.objects.create(
                name="Invalid Course",
                description="This course has an invalid skill level.",
                skill_level="InvalidLevel"
            )

    def test_course_type_unique_name(self):
        """Test that the CourseType name is unique."""
        with self.assertRaises(Exception):
            CourseType.objects.create(
                name="Python Basics",
                description="Duplicate course name.",
                skill_level="Intermediate"
            )
