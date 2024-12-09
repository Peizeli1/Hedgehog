from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Booking, Course, Student



# class LogInForm(forms.Form):
#     """Form enabling registered users to log in."""
#     username = forms.CharField(
#         label="Username",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#     )
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#     )

#     def get_user(self):
#         """Returns authenticated user if possible."""
#         user = None
#         if self.is_valid():
#             username = self.cleaned_data.get('username')
#             password = self.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#         return user


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    def get_user(self):
        """Authenticate and return the user."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
    
class UserForm(forms.ModelForm):
    """Form to update user profiles."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class PasswordForm(forms.Form):
    """Form enabling users to change their password."""
    password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$',
            message='Password must contain at least one uppercase letter, one lowercase letter, and one number.'
        )],
    )
    password_confirmation = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    def __init__(self, user=None, **kwargs):
        """Initialize with user instance."""
        super().__init__(**kwargs)
        self.user = user

    def clean_password(self):
        """Validate the current password."""
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError("The current password is invalid.")
        return password

    def clean(self):
        """Perform overall form validation."""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        password_confirmation = cleaned_data.get('password_confirmation')

        # Check if new password and confirmation match
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Passwords do not match.')

        return cleaned_data

    def save(self):
        """Save the new password."""
        new_password = self.cleaned_data.get('new_password')
        self.user.set_password(new_password)
        self.user.save()
        return self.user



class SignUpForm(UserCreationForm):
    """Form enabling unregistered users to sign up."""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Select Role")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def save(self, commit=True):
        """Create a new user and assign the selected role."""
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  # Assign the selected role
        if commit:
            user.save()
        return user


class StudentBookingForm(forms.ModelForm):
    """Form for students to book a course."""
    class Meta:
        model = Booking
        fields = ['student', 'course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: Setting student field as readonly
        self.fields['student'].widget.attrs.update({'readonly': True})


class CourseEnrollmentForm(forms.Form):
    """Form for enrolling students in courses."""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Student"
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )


class BookingForm(forms.ModelForm):
    """Form for managing bookings between students and courses."""
    class Meta:
        model = Booking
        fields = ['student', 'course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """Custom validation to ensure a student can't book the same course multiple times."""
        super().clean()
        student = self.cleaned_data.get('student')
        course = self.cleaned_data.get('course')

        if Booking.objects.filter(student=student, course=course).exists():
            self.add_error('course', 'This student is already booked for this course.')
