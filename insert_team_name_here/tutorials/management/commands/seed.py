from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from tutorials.models import User
from random import choice
from faker import Faker

class Command(BaseCommand):
    """Build automation command to seed the database."""
    USER_COUNT = 10
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()

    def create_users(self):
        user_fixtures = [
            {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'role': 'admin'},
            {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe', 'role': 'tutor'},
            {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson', 'role': 'student'},
        ]
        
        self.create_groups()
        for data in user_fixtures:
            data['email'] = self.create_unique_email(data['first_name'], data['last_name'])
            data['username'] = self.create_unique_username(data['username'])
            self.try_create_user(data)
        while User.objects.count() < self.USER_COUNT:
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = self.create_unique_email(first_name, last_name)
            username = self.create_unique_username(self.create_username(first_name, last_name))
            role = choice(['tutor', 'student', 'admin'])
            self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'role': role})

    def try_create_user(self, data):
        """Try creating a user and assign a role."""
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=self.DEFAULT_PASSWORD,
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            self.assign_role(user, data['role'])
        except Exception as e:
            print(f"Error creating user {data['username']}: {e}")

    def assign_role(self, user, role):
        """Assign a role to the user based on the role specified."""
        if role == 'admin':
            admin_group, created = Group.objects.get_or_create(name='Admin')
            user.groups.add(admin_group)
        elif role == 'tutor':
            tutor_group, created = Group.objects.get_or_create(name='Tutor')
            user.groups.add(tutor_group)
        elif role == 'student':
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
        user.save()

    def create_groups(self):
        """Create the required groups if they don't exist."""
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='Tutor')
        Group.objects.get_or_create(name='Student')

    def create_username(self, first_name, last_name):
        return '@' + first_name.lower() + last_name.lower()

    def create_email(self, first_name, last_name):
        return first_name + '.' + last_name + '@example.org'

    def create_unique_email(self, first_name, last_name):
        """unique email in case names are the same"""
        email_base = self.create_email(first_name, last_name)
        email = email_base
        counter = 1
        while User.objects.filter(email=email).exists():
            email = f"{email_base.split('@')[0]}{counter}@example.org"
            counter += 1
        return email

    def create_unique_username(self, username):
        """unique username in case names are the same"""
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        return username
