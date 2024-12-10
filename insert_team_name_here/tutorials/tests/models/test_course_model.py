from django.test import TestCase
from tutorials.models import User, Tutor, CourseType, Course

class CourseModelTestCase(TestCase):
    """Unit tests for the Course model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@tutor1',
            first_name='Tutor',
            last_name='One',
            email='tutor1@example.com',
            password='Password123',
            role='tutor'
        )
        self.tutor = Tutor.objects.create(user=self.user, expertise="Python")
        self.course_type = CourseType.objects.create(name="Python Basics", skill_level="Beginner")
        self.course = Course.objects.create(
            tutor=self.tutor,
            course_type=self.course_type,
            day_of_week="Monday",
            time_slot="10:00",
            duration=60,
            location="Room 101",
            status="Scheduled"
        )

    def test_course_creation(self):
        self.assertEqual(self.course.tutor, self.tutor)
        self.assertEqual(self.course.course_type, self.course_type)
        self.assertEqual(self.course.day_of_week, "Monday")
        self.assertEqual(self.course.duration, 60)
        self.assertEqual(self.course.location, "Room 101")
        self.assertEqual(self.course.status, "Scheduled")

    def test_str_representation(self):
        self.assertEqual(str(self.course), "Python Basics (Monday)")
