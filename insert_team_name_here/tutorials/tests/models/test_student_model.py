from django.test import TestCase
from tutorials.models import User, Student

class StudentModelTestCase(TestCase):
    """Unit tests for the Student model."""

    fixtures = ['default_data.json']

    def setUp(self):
        self.user = User.objects.get(username='@student1')
        self.student = Student.objects.create(
            user=self.user,
            phone='1234567890',
            programming_level='Intermediate'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.user, self.user)
        self.assertEqual(self.student.phone, '1234567890')
        self.assertEqual(self.student.programming_level, 'Intermediate')

    def test_str_representation(self):
        self.assertEqual(str(self.student), '@student1 - Intermediate')
