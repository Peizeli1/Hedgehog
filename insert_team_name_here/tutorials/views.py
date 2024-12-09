from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, FormView, UpdateView, TemplateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
import datetime
from .models import Course, Invoice, Notification, Tutor, Student, User, CourseEnrollment
from .forms import LogInForm, PasswordForm, UserForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string


# Helper Functions
def get_next_course(courses):
    """Retrieve the next scheduled course enrollment."""
    now = datetime.datetime.now()
    return courses.filter(course__time_slot__gte=now).order_by('course__time_slot').first()

class RoleRequiredMixin:
    """Mixin to restrict view access based on user role."""
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in self.allowed_roles:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('tutorials:dashboard')  # Redirect unauthorized users to the dashboard
        return super().dispatch(request, *args, **kwargs)


# Mixin for Login-Prohibited Views
# class LoginProhibitedMixin:
#     """Mixin that redirects authenticated users from views intended for unauthenticated users."""
#     redirect_when_logged_in_url = None

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return self.handle_already_logged_in(request, *args, **kwargs)
#         return super().dispatch(request, *args, **kwargs)

#     def handle_already_logged_in(self, request, *args, **kwargs):
#         """Redirect authenticated users to the specified URL."""
#         return redirect(self.get_redirect_when_logged_in_url())

#     def get_redirect_when_logged_in_url(self):
#         """Return the URL to redirect authenticated users."""
#         if self.redirect_when_logged_in_url is None:
#             raise ImproperlyConfigured(
#                 f"{self.__class__.__name__} requires a value for 'redirect_when_logged_in_url'."
#             )
#         return self.redirect_when_logged_in_url

class LoginProhibitedMixin:
    """Mixin that redirects authenticated users from views intended for unauthenticated users."""
    redirect_when_logged_in_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_already_logged_in(request)
        return super().dispatch(request, *args, **kwargs)

    def handle_already_logged_in(self, request):
        """Redirect authenticated users to the specified URL."""
        return redirect(self.get_redirect_when_logged_in_url())

    def get_redirect_when_logged_in_url(self):
        """Return the URL to redirect authenticated users."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires 'redirect_when_logged_in_url' to be defined."
            )
        return self.redirect_when_logged_in_url


class HomeView(View):
    """Display the application's start/home screen."""

    def get(self, request):
        """Handle GET requests."""
        if request.user.is_authenticated:
            return redirect('tutorials:dashboard')
        return render(request, 'home.html')


# class LogInView(LoginProhibitedMixin, View):
#     """Display login screen and handle user login."""
#     redirect_when_logged_in_url = reverse_lazy('tutorials:dashboard')

#     def get(self, request):
#         """Display log in template."""
#         form = LogInForm()
#         return render(request, 'log_in.html', {'form': form, 'next': request.GET.get('next', '')})

#     def post(self, request):
#         """Handle login attempts."""
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user:
#                 login(request, user)
#                 return redirect(request.POST.get('next', self.redirect_when_logged_in_url))
#             messages.error(request, "Invalid username or password.")
#         return render(request, 'log_in.html', {'form': form})

class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""
    redirect_when_logged_in_url = reverse_lazy('tutorials:dashboard')

    def get(self, request):
        """Render the login template with the form."""
        form = LogInForm()
        next_url = request.GET.get('next', '')  # Capture the next URL if provided
        return render(request, 'log_in.html', {'form': form, 'next': next_url})

    def post(self, request):
        """Handle login form submission."""
        form = LogInForm(request.POST)
        next_url = request.POST.get('next') or str(self.redirect_when_logged_in_url)
        if form.is_valid():
            user = form.get_user()
            print(user)
            if user:
                login(request, user)
                return redirect(next_url)
            messages.error(request, "Invalid username or password.")
        return render(request, 'log_in.html', {'form': form, 'next': next_url})

class LogOutView(View):
    """Class-based view to handle user logout."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests to log out the current user."""
        logout(request)
        return redirect('tutorials:home')


# class PasswordView(LoginProhibitedMixin, FormView):
#     """Display password change screen and handle password change requests."""
#     template_name = 'password.html'
#     form_class = PasswordForm
#     redirect_when_logged_in_url = reverse_lazy('tutorials:dashboard')

#     def get_form_kwargs(self, **kwargs):
#         """Pass the current user to the password change form."""
#         kwargs = super().get_form_kwargs(**kwargs)
#         kwargs.update({'user': self.request.user})
#         return kwargs

#     def form_valid(self, form):
#         """Handle valid form by saving the new password."""
#         form.save()
#         login(self.request, self.request.user)
#         messages.success(self.request, "Password updated successfully!")
#         return super().form_valid(form)

#     def get_success_url(self):
#         """Redirect the user after a successful password change."""
#         return reverse_lazy('tutorials:dashboard')

# class PasswordView(FormView):
#     """Display password change screen and handle password change requests."""
#     template_name = 'password.html'
#     form_class = PasswordForm

#     def get_form_kwargs(self, **kwargs):
#         """Pass the current user to the password change form."""
#         kwargs = super().get_form_kwargs(**kwargs)
#         kwargs.update({'user': self.request.user})
#         return kwargs

#     def form_valid(self, form):
#         """Handle valid form by saving the new password."""
#         form.save()
#         messages.success(self.request, "Password updated successfully!")
#         return super().form_valid(form)

#     def get_success_url(self):
#         """Redirect the user after a successful password change."""
#         return reverse_lazy('tutorials:dashboard')


class PasswordView(FormView):
    """Display password change screen and handle password change requests."""
    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""
        form.save()
        messages.success(self.request, "Password updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after a successful password change."""
        return reverse_lazy('tutorials:dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""
    model = User
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        return self.request.user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.success(self.request, "Profile updated!")
        return reverse_lazy('tutorials:dashboard')


class SignUpView(LoginProhibitedMixin, View):
    """Display the sign up screen and handle user registration."""
    redirect_when_logged_in_url = reverse_lazy('tutorials:dashboard')

    def get(self, request):
        """Display sign up form."""
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        """Handle sign up form submission."""
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Notification.objects.create(
                user=user,
                message="Welcome to Hedgehog Tutoring! Start exploring your dashboard and profile.",
                is_read=False
            )
            login(request, user)
            return redirect(self.redirect_when_logged_in_url)
        return render(request, 'sign_up.html', {'form': form})


class DashboardView(LoginRequiredMixin, TemplateView):
    """Display the user's dashboard."""
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        """Generate the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == 'student':
            # Get the student object linked to the logged-in user
            student = get_object_or_404(Student, user=user)

            # Query for available courses
            available_courses = Course.objects.filter(
                tutor__is_available=True,  # Tutors must be available
                course_type__skill_level=student.programming_level  # Match student's level
            ).exclude(enrollments__student=student)  # Exclude courses the student is already enrolled in

            # Other data for the dashboard
            unread_notifications_count = user.notifications.filter(is_read=False).count()
            course_count = CourseEnrollment.objects.filter(student=student).count()
            next_course = CourseEnrollment.objects.filter(student=student).order_by('course__time_slot').first()

            context.update({
                'unread_notifications_count': unread_notifications_count,
                'course_count': course_count,
                'next_course_datetime': next_course.course.time_slot if next_course else None,
                'next_course_name': next_course.course.course_type.name if next_course else None,
                'available_courses': available_courses,
                'invoices': student.invoice_set.all(),
            })

        elif user.role == 'tutor':
            tutor = get_object_or_404(Tutor, user=user)
            courses = Course.objects.filter(tutor=tutor)
            context.update({'courses': courses})

        elif user.role == 'admin':
            pass  # No additional data for admin

        return context

    def dispatch(self, request, *args, **kwargs):
        """Redirect non-authenticated users to the login page."""
        user = request.user
        if user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('tutorials:log_in')


class StudentListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """List all students."""
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    allowed_roles = ['admin', 'tutor'] 

    def get_queryset(self):
        return super().get_queryset().order_by('user__last_name')


class TutorListView(LoginRequiredMixin, ListView):
    """List all tutors."""
    model = Tutor
    template_name = 'tutor_list.html'
    context_object_name = 'tutors'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').prefetch_related('advanced_courses').order_by('user__last_name')
        print("Debug: Queryset contains the following tutors:", queryset)  # Debugging output
        return queryset



class CourseBookingView(LoginRequiredMixin, TemplateView):
    print("inside course booking view.")
    """Class-based view to handle course booking."""
    template_name = 'course_booking.html'

    def get_context_data(self, **kwargs):
        """Generate the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        context['available_courses'] = Course.objects.filter(tutor__is_available=True).select_related('tutor', 'course_type')
        return context

    def post(self, request):
        """Handle POST requests for booking a course."""
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        if CourseEnrollment.objects.filter(student=student, course=course).exists():
            messages.error(request, "You have already booked this course.")
        else:
            CourseEnrollment.objects.create(student=student, course=course, status='Active')
            messages.success(request, "Course booked successfully!")
        return redirect('tutorials:dashboard')


class InvoiceView(LoginRequiredMixin, TemplateView):
    """Class-based view to handle invoice-related operations."""
    template_name = 'invoice.html'

    def get_context_data(self, **kwargs):
        """Generate the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == 'student':
            student = get_object_or_404(Student, user=user)
            context['invoices'] = Invoice.objects.filter(student=student)

        elif user.role == 'admin':
            context['invoices'] = Invoice.objects.all()

        return context

    def dispatch(self, request, *args, **kwargs):
        """Handle dispatching based on the user's role."""
        user = request.user
        if user.role not in ['student', 'admin']:
            return redirect('tutorials:dashboard')
        return super().dispatch(request, *args, **kwargs)


class CourseBookingConfirmView(LoginRequiredMixin, TemplateView):
    """View to handle confirmation of course booking."""
    template_name = 'course_booking_confirm.html'

    def get_context_data(self, **kwargs):
        """Prepare context data for the template."""
        context = super().get_context_data(**kwargs)
        course_id = kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        context['course'] = course
        return context

    def get(self, request, *args, **kwargs):
        """Handle AJAX GET requests for modal content."""
        context = self.get_context_data(**kwargs)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX
            html = render_to_string(self.template_name, context, request=request)
            return HttpResponse(html)  # Return raw HTML for the modal
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle the course booking confirmation."""
        course_id = kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        if request.user.role != 'student':
            messages.error(request, 'Only students can book courses.')
            return redirect('tutorials:dashboard')

        student = get_object_or_404(Student, user=request.user)

        if CourseEnrollment.objects.filter(student=student, course=course).exists():
            messages.error(request, 'You are already enrolled in this course.')
        else:
            CourseEnrollment.objects.create(student=student, course=course, status='Active')
            messages.success(request, 'Course booked successfully!')

        # Redirect to the dashboard regardless of outcome
        return redirect('tutorials:dashboard')
    

class NotificationsView(LoginRequiredMixin, View):
    """Handle notification-related requests."""
    
    def get(self, request):
        """Handle AJAX GET requests to fetch notifications."""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            notifications = Notification.objects.filter(user=request.user)
            return JsonResponse({
                'notifications': [
                    {
                        'id': notification.id,
                        'message': notification.message,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for notification in notifications
                ]
            })
        return JsonResponse({'error': 'Invalid request'}, status=400)

    def post(self, request):
        """Handle AJAX POST requests to mark a notification as read."""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            notification_id = request.POST.get('notification_id')
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.mark_as_read()  # Mark notification as read
            unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
            return JsonResponse({'success': True, 'unread_count': unread_count})
        return JsonResponse({'error': 'Invalid request'}, status=400)