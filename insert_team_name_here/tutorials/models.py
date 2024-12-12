from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from . import utils


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('admin', 'Admin'),
    ]

    username_validator = RegexValidator(
        regex=r'^@[a-zA-Z0-9]{3,}$',
        message='Username must start with @ followed by at least three alphanumeric characters, '
                'and cannot include special characters except @.'
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='student',
        help_text="Defines the user's role (Student, Tutor, or Admin)."
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        return utils.get_gravatar_url(self.email, size)

    def mini_gravatar(self):
        return utils.get_mini_gravatar_url(self.email)

    def __str__(self):
        return f"{self.full_name()} (@{self.username}) - {self.get_role_display()}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}{'...' if len(self.message) > 20 else ''}"

    def mark_as_read(self):
        """Mark this notification as read."""
        self.is_read = True
        self.save()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    phone_validator = RegexValidator(
        regex=r'^[0-9 -]+$',
        message='Phone number should only contain digits, spaces, and hyphens.'
    )
    phone = models.CharField(max_length=20, validators=[phone_validator])
    notes = models.TextField(blank=True, null=True)
    programming_level = models.CharField(
        max_length=50,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner',
        help_text="The programming level of the student."
    )

    def __str__(self):
        return self.user.full_name()


class CourseType(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Course name, e.g., 'Web Development with Ruby on Rails'.")
    description = models.TextField(help_text="Detailed description of the course.")
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ],
        default='Beginner',
        help_text="Skill level required for the course."
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this field

    def __str__(self):
        return self.name


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tutor'})
    expertise = models.CharField(max_length=255, help_text="e.g., Python, JavaScript, Ruby.")
    is_available = models.BooleanField(default=True, help_text="Indicates whether the tutor is available.")
    advanced_courses = models.ManyToManyField(
        CourseType,
        blank=True,
        help_text="List of advanced courses the tutor can teach."
    )

    def __str__(self):
        return self.user.full_name()


class Course(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses_taught')
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        related_name='courses_offered',
        help_text="The type of course being taught."
    )
    day_of_week = models.CharField(max_length=10, help_text="e.g., Monday, Tuesday.")
    time_slot = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes.")
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Scheduled", help_text="e.g., Scheduled, Cancelled.")

    def __str__(self):
        return f"{self.course_type.name} ({self.day_of_week})"


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.full_name()} booked {self.course.course_type.name}"


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Active',
        help_text="The current status of the enrollment."
    )

    def __str__(self):
        return f"{self.student.user.full_name()} - {self.course.course_type.name}"


class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id}: {self.student.user.full_name()} - Amount: {self.amount}, Due: {self.due_date}, Status: {self.status}"

class StudentRequest(models.Model):
    STATUS_CHOICES = [
        ('unallocated', 'Unallocated'),
        ('allocated', 'Allocated'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unallocated')
    created_at = models.DateTimeField(auto_now_add=True)
    allocated_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocated_requests'
    )
    admin_reply = models.TextField(blank=True, null=True, help_text="Reply provided by the admin.")  
    replied_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies',
        help_text="Admin who provided the reply."
    )

    def __str__(self):
        return f"Request by {self.student.username} - {self.status}"
    
class RequestReply(models.Model):
    student_request = models.ForeignKey(
        StudentRequest, on_delete=models.CASCADE, related_name='replies'
    )
    replied_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'admin'}
    )
    reply_text = models.TextField(help_text="The text of the admin's reply.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.replied_by.username} on Request {self.student_request.id}"
