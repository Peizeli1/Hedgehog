from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import Group
from tutorials.models import User, Student, Tutor, CourseType, Course, Invoice, CourseEnrollment, Booking
from faker import Faker
import random
from datetime import timedelta, datetime
from django.contrib.auth.hashers import make_password

fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with sample data'

    ADMIN_COUNT = 2
    TUTOR_COUNT = 5
    STUDENT_COUNT = 10
    DEFAULT_PASSWORD = 'Password123'
    
    def handle(self, *args, **kwargs):
        """Main entry point for the seed script."""
        self.clear_data()
        self.create_groups()

        with transaction.atomic():
            self.create_admins()
        
        # Create specific users
        self.create_specific_users()

        course_types = self.create_course_types()  # Create course types before tutors
        tutors = self.create_tutors()             # Tutors can now use course types
        students = self.create_students()         # Students are independent of course types
        courses = self.create_courses(tutors, course_types)  # Courses depend on tutors and course types
        self.create_bookings(students, courses)   # Bookings depend on students and courses
        self.create_enrollments(students, courses)  # Enrollments depend on students and courses
        self.create_invoices(students)           # Invoices depend on students

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def clear_data(self):
        """Clear existing data from the database."""
        Booking.objects.all().delete()
        Invoice.objects.all().delete()
        CourseEnrollment.objects.all().delete()
        Course.objects.all().delete()
        CourseType.objects.all().delete()
        Student.objects.all().delete()
        Tutor.objects.all().delete()
        User.objects.all().delete()  # Delete Users last to avoid FK constraint issues
        self.stdout.write(self.style.WARNING('Cleared all existing data!'))

    def create_groups(self):
        """Create required groups if they don't already exist."""
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='Tutor')
        Group.objects.get_or_create(name='Student')

    def create_admins(self):
        """Create sample admin users."""
        for _ in range(self.ADMIN_COUNT):
            try:
                first_name = fake.first_name()
                last_name = fake.last_name()
                username = self.create_unique_username(f"@{first_name.lower()}{last_name.lower()}")
                email = self.create_unique_email(first_name, last_name)
                self.stdout.write(self.style.WARNING(f"Creating Admin with username: {username}, email: {email}"))
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=self.DEFAULT_PASSWORD,
                    first_name=first_name,
                    last_name=last_name,
                    role='admin',
                )
                admin_group = Group.objects.get(name='Admin')
                user.groups.add(admin_group)
                self.stdout.write(self.style.SUCCESS(f'Admin user created: {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating admin user: {e}"))
    
    
    def create_specific_users(self):
        """Create specific users for testing."""
        specific_users = [
            {"username": "@johndoe", "role": "admin", "first_name": "John", "last_name": "Doe"},
            {"username": "@janedoe", "role": "tutor", "first_name": "Jane", "last_name": "Doe"},
            {"username": "@charlie", "role": "student", "first_name": "Charlie", "last_name": ""},
        ]

        for user_data in specific_users:
            try:
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        "first_name": user_data['first_name'],
                        "last_name": user_data['last_name'],
                        "email": self.create_unique_email(user_data['first_name'], user_data['last_name']),
                        "role": user_data['role'],
                    },
                )

                if created:
                    user.set_password(self.DEFAULT_PASSWORD)  # Properly hash the password
                    user.save()

                if user_data['role'] == 'tutor':
                    Tutor.objects.get_or_create(user=user)
                elif user_data['role'] == 'student':
                    Student.objects.get_or_create(user=user)

                self.stdout.write(self.style.SUCCESS(f"Specific user created: {user.username}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating specific user {user_data['username']}: {e}"))


    def create_tutors(self):
        """Create sample tutor users."""
        tutors = []
        all_course_types = list(CourseType.objects.all())  # Retrieve all course types to assign as advanced courses
        predefined_expertise = ['Python', 'JavaScript', 'Ruby', 'Data Science', 'Machine Learning', 'Java', 'C++']

        if not all_course_types:
            self.stdout.write(self.style.ERROR("No course types available to assign as advanced courses. Create course types first."))
            return tutors

        for _ in range(self.TUTOR_COUNT):
            try:
                with transaction.atomic():
                    # Generate unique names, username, and email
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    username = self.create_unique_username(f"@{first_name.lower()}{last_name.lower()}")
                    email = self.create_unique_email(first_name, last_name)
                    self.stdout.write(self.style.WARNING(f"Creating Tutor with username: {username}, email: {email}"))

                    # Create or get the user
                    user, created = User.objects.get_or_create(
                        username=username,
                        email=email,
                        defaults={
                            "password": make_password(self.DEFAULT_PASSWORD),
                            "first_name": first_name,
                            "last_name": last_name,
                            "role": "tutor",
                        },
                    )

                    # Check if a Tutor object already exists for this user
                    tutor, tutor_created = Tutor.objects.get_or_create(
                        user=user,
                    )
                    
                    tutor.expertise = random.choice(predefined_expertise)
                    tutor.is_available = random.choice([True, False])

                    # Always ensure advanced courses are set
                    if not tutor.advanced_courses.exists():
                        num_courses = random.randint(1, 3)  # Assign 1 to 3 advanced courses
                        advanced_courses = random.sample(all_course_types, k=num_courses)
                        tutor.advanced_courses.set(advanced_courses)  # Assign advanced courses
                        
                        tutor.save()
                        self.stdout.write(self.style.SUCCESS(f"Tutor updated: {user.username} with {num_courses} advanced courses."))

                    tutors.append(tutor)

                    if tutor_created:
                        self.stdout.write(self.style.SUCCESS(f"New tutor created: {user.username} with expertise in {tutor.expertise}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Existing tutor found: {user.username} with expertise in {tutor.expertise}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating or updating tutor user: {e}"))

        return tutors
    
    
    def create_students(self):
        """Create sample student users."""
        students = []

        for _ in range(self.STUDENT_COUNT):
            try:
                with transaction.atomic():
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    username = self.create_unique_username(f"@{first_name.lower()}{last_name.lower()}")
                    email = self.create_unique_email(first_name, last_name)
                    self.stdout.write(self.style.WARNING(f"Creating Student with username: {username}, email: {email}"))

                    # Create or get the user
                    user, created = User.objects.get_or_create(
                        username=username,
                        email=email,
                        defaults={
                            "password": make_password(self.DEFAULT_PASSWORD),
                            "first_name": first_name,
                            "last_name": last_name,
                            "role": "student",
                        },
                    )

                    # Check if a Student object already exists for this user
                    student, student_created = Student.objects.get_or_create(
                        user=user,
                        defaults={
                            "phone": fake.phone_number(),
                            "programming_level": random.choice(['Beginner', 'Intermediate', 'Advanced']),
                        },
                    )

                    # If the student already exists, update the phone and programming level
                    if not student_created:
                        student.phone = fake.phone_number()
                        student.programming_level = random.choice(['Beginner', 'Intermediate', 'Advanced'])
                        student.save()
                        self.stdout.write(self.style.WARNING(f"Existing student updated: {user.username}"))

                    students.append(student)

                    if student_created:
                        self.stdout.write(self.style.SUCCESS(f"New student created: {user.username}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Existing student found: {user.username}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating or updating student user: {e}"))

        return students


    def create_course_types(self):
        """Create sample course types with random costs."""
        course_types = []
        for _ in range(5):  
            try:
                course_type = CourseType.objects.create(
                    name=fake.word().capitalize(),
                    description=fake.sentence(),
                    skill_level=random.choice(['Beginner', 'Intermediate', 'Advanced']),
                    cost=round(random.uniform(50, 200), 2),  
                )
                course_types.append(course_type)
                self.stdout.write(self.style.SUCCESS(f'Course type created: {course_type.name} with cost ${course_type.cost}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating course type: {e}"))
        return course_types

    def create_courses(self, tutors, course_types):
        """Create sample courses."""
        courses = []
        if not tutors or not course_types:
            self.stdout.write(self.style.ERROR("No tutors or course types available to create courses."))
            return courses

        for _ in range(10):  # You can adjust the number of courses as needed
            try:
                tutor = random.choice(tutors)
                course_type = random.choice(course_types)
                course = Course.objects.create(
                    tutor=tutor,
                    course_type=course_type,
                    day_of_week=random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                    time_slot=fake.time(),
                    duration=random.randint(30, 120),
                    location=fake.address(),
                    status=random.choice(['Scheduled', 'Cancelled']),
                )
                courses.append(course)
                self.stdout.write(self.style.SUCCESS(f'Course created: {course.course_type.name} with cost ${course.course_type.cost}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating course: {e}"))
        return courses

    def create_bookings(self, students, courses):
        """Create bookings for students."""
        for student in students:
            try:
                booked_courses = random.sample(courses, k=min(len(courses), random.randint(1, 2)))
                for course in booked_courses:
                    Booking.objects.create(
                        student=student,
                        course=course
                    )
                    self.stdout.write(self.style.SUCCESS(f"Booking created: {student.user.username} booked {course.course_type.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating booking: {e}"))

    def create_enrollments(self, students, courses):
        """Enroll students in courses."""
        for student in students:
            try:
                available_courses = [course for course in courses if course.course_type.skill_level == student.programming_level]
                if not available_courses:
                    continue
                enrolled_courses = random.sample(available_courses, k=min(len(available_courses), random.randint(1, 3)))
                for course in enrolled_courses:
                    CourseEnrollment.objects.create(
                        student=student,
                        course=course,
                        status=random.choice(['Active', 'Completed', 'Cancelled']),
                    )
                self.stdout.write(self.style.SUCCESS(f'Student enrolled: {student.user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error enrolling student: {e}"))

    
    def create_invoices(self, students):
        """Generate invoices for students."""
        for student in students:
            enrollments = CourseEnrollment.objects.filter(student=student, status='Active')
            if not enrollments.exists():
                self.stdout.write(self.style.WARNING(f"No active enrollments for student {student.user.username}. Skipping invoice generation."))
                continue

            for enrollment in enrollments:
                try:
                    Invoice.objects.create(
                        student=student,
                        course=enrollment.course,
                        amount=enrollment.course.course_type.cost,  # Use the course type's cost
                        status=random.choice(['Paid', 'Unpaid']),
                        due_date=datetime.now() + timedelta(days=random.randint(10, 30)),
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Invoice created for student {student.user.username} for course {enrollment.course.course_type.name} with cost ${enrollment.course.course_type.cost}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating invoice for student {student.user.username}: {e}"))

    def create_unique_email(self, first_name, last_name):
        """Ensure unique email addresses."""
        email_base = f"{first_name.lower()}.{last_name.lower()}@example.org"
        email = email_base
        counter = 1
        while User.objects.filter(email=email).exists():
            email = f"{email_base.split('@')[0]}{counter}@example.org"
            counter += 1
        return email

    def create_unique_username(self, username):
        """Ensure unique usernames."""
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        return username
