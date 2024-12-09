from django.core.management.base import BaseCommand
from tutorials.models import User, Student, Tutor, CourseType, Course, Invoice, CourseEnrollment
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Remove all seeded data from the database'

    def handle(self, *args, **kwargs):
        self.clear_data()
        self.stdout.write(self.style.SUCCESS('Database unseeded successfully!'))

    def clear_data(self):
        """Remove all data created by the seed script."""
        # Clear specific models in reverse dependency order
        Invoice.objects.all().delete()
        CourseEnrollment.objects.all().delete()  # New: Clear enrollments before courses
        Course.objects.all().delete()
        CourseType.objects.all().delete()
        Student.objects.all().delete()
        Tutor.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()  # Keep superuser accounts

        # Clear groups created by seed
        Group.objects.filter(name__in=['Admin', 'Tutor', 'Student']).delete()

        self.stdout.write(self.style.WARNING('All seeded data, enrollments, and groups have been deleted!'))
