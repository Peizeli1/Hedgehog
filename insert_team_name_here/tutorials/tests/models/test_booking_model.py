from django.test import TestCase
from tutorials.models import User, Student, Tutor, CourseType, Course, Booking

class BookingModelTestCase(TestCase):
    """Unit tests for the Booking model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@student1',
            first_name='Student',
            last_name='One',
            email='student1@example.com',
            password='Password123',
            role='student'
        )
        self.student = Student.objects.create(user=self.user)
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
        self.booking = Booking.objects.create(student=self.student, course=self.course)

    def test_booking_creation(self):
        self.assertEqual(self.booking.student, self.student)
        self.assertEqual(self.booking.course, self.course)

    def test_str_representation(self):
        self.assertEqual(
            str(self.booking),
            "Student One booked Python Basics"
        )
