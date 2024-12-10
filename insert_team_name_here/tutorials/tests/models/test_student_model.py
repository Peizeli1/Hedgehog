from django.test import TestCase
from tutorials.models import User, Student

class StudentModelTestCase(TestCase):
    """Unit tests for the Student model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@student1',
            first_name='Student',
            last_name='One',
            email='student1@example.com',
            password='Password123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            phone='123-456-7890',
            programming_level='Intermediate'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.user, self.user)
        self.assertEqual(self.student.phone, '123-456-7890')
        self.assertEqual(self.student.programming_level, 'Intermediate')

    def test_str_representation(self):
        self.assertEqual(str(self.student), self.user.full_name())
