"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User
from .models import Booking


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user


class StudentBookingForm(forms.ModelForm):
    """Form for students to book a slot."""

    class Meta:
        model = Booking
        fields = ['student', 'course']

        widgets = {
            'studentdescription': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Add a note or details about your booking.'}),
        }

    def __init__(self, *args, **kwargs):
        """Custom initialization for form."""
        super().__init__(*args, **kwargs)
        # Example: Setting placeholder text or making fields read-only
        self.fields['student'].widget.attrs.update({'readonly': True})


class TutorsActionForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('calendar', 'Calendar'),
            ('profile', 'Edit Profile'),
            ('invoices', 'Invoices'),
            ('log_out', 'Log Out'),
            ('requests', 'Requests')
        ],
        widget=forms.RadioSelect,
    )
    
class InvoiceForm(forms.Form):
    invoice_id = forms.IntegerField(
        required=False,
        label="Invoice ID",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Invoice ID'}),
    )
    action = forms.ChoiceField(
        choices=[
            ('view', 'View Invoice'),
            ('download', 'Download Invoice'),
        ],
        widget=forms.Select,
        required=True,
    )

class CalendarFilterForm(forms.Form):
    month = forms.ChoiceField(
        choices=[
            (1, 'January'), (2, 'February'), (3, 'March'),
            (4, 'April'), (5, 'May'), (6, 'June'),
            (7, 'July'), (8, 'August'), (9, 'September'),
            (10, 'October'), (11, 'November'), (12, 'December')
        ],
        label="Select Month",
        required=True,
        widget=forms.Select,
    )
    year = forms.IntegerField(
        label="Year",
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Year'}),
    )


