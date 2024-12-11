from django.test import TestCase
from tutorials.models import Course, Tutor, CourseType

class CourseModelTestCase(TestCase):
    """Unit tests for the Course model."""

    fixtures = ['default_data.json']

    def setUp(self):
        self.tutor = Tutor.objects.get(user__username='@tutor1')
        self.course_type = CourseType.objects.get(name='Python Basics')
        self.course = Course.objects.create(
            tutor=self.tutor,
            course_type=self.course_type,
            day_of_week='Monday',
            time_slot='10:00:00',
            duration=60,
            location='Room 101',
            status='Scheduled'
        )

    def test_course_creation(self):
        self.assertEqual(self.course.tutor, self.tutor)
        self.assertEqual(self.course.course_type, self.course_type)
        self.assertEqual(self.course.day_of_week, 'Monday')

    def test_str_representation(self):
        self.assertEqual(str(self.course), 'Python Basics - Monday at 10:00 AM')
