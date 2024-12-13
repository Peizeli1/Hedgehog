from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, FormView, UpdateView, TemplateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from datetime import datetime, date, time, timedelta
from calendar import monthrange
from .models import Course, Invoice, Notification, Tutor, Student, User, CourseEnrollment, StudentRequest, RequestReply
from .forms import LogInForm, PasswordForm, UserForm, SignUpForm, StudentRequestForm, UpdateRequestForm
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
            return redirect('tutorials:dashboard')
        return super().dispatch(request, *args, **kwargs)


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


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""
    redirect_when_logged_in_url = reverse_lazy('tutorials:dashboard')

    def get(self, request):
        """Render the login template with the form."""
        form = LogInForm()
        next_url = request.GET.get('next', '')
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
        """Provide context for the dashboard."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = datetime.now()
        year, month = now.year, now.month

        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_notifications_count = notifications.filter(is_read=False).count()

        context['notifications'] = notifications
        context['unread_notifications_count'] = unread_notifications_count

        context['month'] = now.strftime('%B')
        context['year'] = year

        if user.role == 'student':
            student = user.student

            available_courses = Course.objects.filter(
                tutor__is_available=True,
                course_type__skill_level=student.programming_level
            ).exclude(enrollments__student=student)
            context['available_courses'] = available_courses

            context['course_count'] = CourseEnrollment.objects.filter(student=student).count()
            next_course = CourseEnrollment.objects.filter(student=student, status='Active').order_by(
                'course__time_slot').first()

            events_by_day, today = self.generate_calendar_events(student, year, month)
            context['events_by_day'] = events_by_day
            context['today'] = today

            context['next_course_datetime'] = next_course.course.time_slot if next_course else "No upcoming courses"
            context['next_course_name'] = next_course.course.course_type.name if next_course else "N/A"

            context['invoices'] = Invoice.objects.filter(student=student, status='Unpaid').order_by('due_date')

        elif user.role == 'tutor':
            tutor = get_object_or_404(Tutor, user=user)

            courses = Course.objects.filter(tutor=tutor)

            events_by_day, today = self.generate_calendar_events_for_tutor(tutor, year, month)

            context.update({
                'courses': courses,
                'events_by_day': events_by_day,
                'today': today,
                'next_course_datetime': 'N/A',
                'next_course_name': 'N/A',
                'invoices': []
            })

        elif user.role == 'admin':
            all_students = Student.objects.all()
            all_enrollments = CourseEnrollment.objects.select_related('course', 'student').filter(
                student__in=all_students).order_by('course__time_slot')

            events_by_day, today = self.generate_calendar_events_for_admin(all_students, year, month)
            context['events_by_day'] = events_by_day
            context['today'] = today
            context['invoices'] = Invoice.objects.filter(status='Unpaid').order_by('due_date')
            context['all_courses'] = Course.objects.all()
            context['all_bookings'] = all_enrollments

        return context

    def generate_calendar_events(self, student, year, month):
        """Generate calendar events for the student."""
        return self._generate_calendar_events_for_user(student.user, year, month)

    def generate_calendar_events_for_tutor(self, tutor, year, month):
        """Generate calendar events for the tutor."""
        return self._generate_calendar_events_for_user(tutor.user, year, month)

    def generate_calendar_events_for_admin(self, students, year, month):
        """Generate calendar events for all students (for admin view)."""
        events_by_day = {}
        today = date.today()
        for student in students:
            enrollments = CourseEnrollment.objects.filter(student=student)
            for enrollment in enrollments:
                course = enrollment.course
                course_date = self.get_course_date_for_month(course, year, month, today)

                if course_date and course_date.month == month and course_date.year == year and course_date >= today:
                    if course_date not in events_by_day:
                        events_by_day[course_date] = []

                    events_by_day[course_date].append(
                        {
                            "course_name": course.course_type.name,
                            "student_name": student.user.get_full_name(),
                            "time": course.time_slot.strftime("%H:%M %p"),
                            "status": self.get_event_status(
                                datetime.combine(course_date, datetime.min.time()) if isinstance(course_date,
                                                                                                 date) else course_date),
                            "tutor_name": course.tutor.user.get_full_name(),
                        }
                    )

        calendar_days = []
        days_in_month = monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            day_date = date(year, month, day)
            day_events = events_by_day.get(day_date, [])
            calendar_days.append({"day": day_date, "events": day_events})

        return calendar_days, today

    def _generate_calendar_events_for_user(self, user, year, month):
        """Helper function to generate calendar events for a user (student or tutor)."""
        days_in_month = monthrange(year, month)[1]
        today = date.today()

        events_by_day = {}

        if user.role == 'student':
            enrollments = CourseEnrollment.objects.filter(student__user=user)
            for enrollment in enrollments:
                course = enrollment.course
                course_date = self.get_course_date_for_month(course, year, month, today)

                if course_date and course_date.month == month and course_date.year == year and course_date >= today:
                    if course_date not in events_by_day:
                        events_by_day[course_date] = []

                    events_by_day[course_date].append(
                        {
                            "course_name": course.course_type.name,
                            "time": course.time_slot.strftime("%H:%M %p"),
                            "status": self.get_event_status(datetime.combine(course_date, course.time_slot)),
                        }
                    )
        elif user.role == 'tutor':
            courses = Course.objects.filter(tutor__user=user)
            for course in courses:
                course_date = self.get_course_date_for_month(course, year, month, today)

                if course_date and course_date.month == month and course_date.year == year and course_date >= today:
                    if course_date not in events_by_day:
                        events_by_day[course_date] = []
                    for enrollment in CourseEnrollment.objects.filter(course=course):
                        student_name = enrollment.student.user.get_full_name()
                        events_by_day[course_date].append(
                            {
                                "course_name": course.course_type.name,
                                "time": course.time_slot.strftime("%H:%M %p"),
                                "status": self.get_event_status(course_date),
                                "student_name": student_name,
                            }
                        )

        calendar_days = []
        for day in range(1, days_in_month + 1):
            day_date = date(year, month, day)
            day_events = events_by_day.get(day_date, [])
            calendar_days.append({"day": day_date, "events": day_events})

        return calendar_days, today

    def get_course_date_for_month(self, course, year, month, today):
        """Calculate the actual date for the course based on its day_of_week."""
        days_of_week = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }

        first_day_of_month = date(year, month, 1)
        target_weekday = days_of_week.get(course.day_of_week, None)

        if target_weekday is None:
            return None

        day_difference = (target_weekday - first_day_of_month.weekday()) % 7
        course_date = first_day_of_month + timedelta(days=day_difference)

        while course_date < today:
            course_date += timedelta(weeks=1)

        if course_date.month == month and course_date.year == year:
            return course_date

        return None

    def get_event_status(self, event_datetime):
        """Determine the status of an event based on its datetime."""
        now = datetime.now()
        if isinstance(event_datetime, date) and not isinstance(event_datetime, datetime):
            event_datetime = datetime.combine(event_datetime, datetime.min.time())
        if event_datetime > now:
            return "Upcoming"
        return "Completed"

    def dispatch(self, request, *args, **kwargs):
        """Redirect non-authenticated users to the login page."""
        if request.user.is_authenticated:
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
        queryset = super().get_queryset().select_related('user').prefetch_related('advanced_courses').order_by(
            'user__last_name')
        print("Debug: Queryset contains the following tutors:", queryset)
        return queryset


class CourseBookingView(LoginRequiredMixin, TemplateView):
    """Class-based view to handle course booking."""
    template_name = 'course_booking.html'

    def get_context_data(self, **kwargs):
        """Generate the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        context['available_courses'] = Course.objects.filter(tutor__is_available=True).select_related('tutor',
                                                                                                      'course_type')
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

            notification_message = f"You have successfully booked the course '{course.course_type.name}' scheduled on {course.day_of_week} at {course.time_slot}."
            print(notification_message)
            Notification.objects.create(
                user=student.user,
                message=notification_message,
                is_read=False,
            )

            messages.success(request, "Course booked successfully!")

        return redirect('tutorials:dashboard')


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

            due_date = datetime.now() + timedelta(days=30)
            invoice = Invoice.objects.create(
                student=student,
                course=course,
                amount=course.course_type.cost,
                status='Unpaid',
                due_date=due_date
            )

            notification_message = f"You have successfully booked the course '{course.course_type.name}' scheduled on {course.day_of_week} at {course.time_slot}."
            Notification.objects.create(
                user=student.user,
                message=notification_message,
                is_read=False,
            )

            Notification.objects.create(
                user=student.user,
                message=f"Invoice for the course '{course.course_type.name}' is due on {invoice.due_date.strftime('%Y-%m-%d')}.",
                is_read=False,
            )

            messages.success(request, "Course booked successfully! An invoice has been generated.")

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
            notification.mark_as_read()
            unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
            return JsonResponse({'success': True, 'unread_count': unread_count})
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def request_list(request):
    if request.user.role == 'student':
        requests = StudentRequest.objects.filter(student=request.user).prefetch_related('replies__replied_by')
    elif request.user.role == 'admin':
        requests = StudentRequest.objects.all().prefetch_related('replies__replied_by')
    else:
        return redirect('tutorials:dashboard')
    return render(request, 'requests/request_list.html', {'requests': requests, 'user': request.user})


@login_required
def create_request(request):
    if request.method == 'POST':
        form = StudentRequestForm(request.POST)
        if form.is_valid():
            student_request = form.save(commit=False)
            student_request.student = request.user
            student_request.status = 'unallocated'
            student_request.save()
            messages.success(request, "Request successfully created!")
            return redirect('tutorials:request_list')
    else:
        form = StudentRequestForm()

    return render(request, 'requests/create_request.html', {'form': form})


@login_required
def update_request_status(request, request_id):
    student_request = get_object_or_404(StudentRequest, id=request_id)
    if request.user.role != 'admin':
        return redirect('tutorials:dashboard')

    if request.method == 'POST':
        form = UpdateRequestForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data.get('admin_reply')
            if reply_text:
                RequestReply.objects.create(
                    student_request=student_request,
                    replied_by=request.user,
                    reply_text=reply_text,
                )

            student_request.status = form.cleaned_data.get('status')
            student_request.allocated_to = form.cleaned_data.get('allocated_to')
            student_request.save()

            messages.success(request, "Request updated successfully!")
            return redirect('tutorials:request_list')
    else:
        form = UpdateRequestForm(instance=student_request)

    replies = student_request.replies.all()

    return render(request, 'requests/update_status.html', {
        'form': form,
        'student_request': student_request,
        'replies': replies,
    })
