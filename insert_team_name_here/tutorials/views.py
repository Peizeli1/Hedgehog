import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm
from tutorials.helpers import login_prohibited
from.models import User, Course, CourseEnrollment, Invoice, Tutor, Student
from django.views.generic import ListView
# from tutorials.views import dashboard
# from tutorials.views.views import LogInView
from. import dashboard_utils  # 导入新创建的模块
from django.contrib.auth.forms import AuthenticationForm

# def get_user_data(user):
#     """获取用户相关数据的函数"""
#     unread_notifications_count = user.notifications.filter(is_read=False).count()
#     course_count = CourseEnrollment.objects.filter(student=user).count()
#
#     now = datetime.datetime.now()
#     enrollments = CourseEnrollment.objects.filter(student=user)
#     next_course = None
#     for enrollment in enrollments:
#         if enrollment.start_date >= now:
#             next_course = enrollment.course
#             break
#
#     next_course_datetime = None
#     next_course_name = None
#     if next_course:
#         next_course_datetime = next_course.start_date
#         next_course_name = next_course.name
#
#     return {
#         'unread_notifications_count': unread_notifications_count,
#         'course_count': course_count,
#         'next_course_datetime': next_course_datetime,
#         'next_course_name': next_course_name
#     }


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    from tutorials.views import dashboard  # 在这里进行延迟导入
    user = request.user

    # 获取未读通知数量
    #unread_notifications_count = user.notifications.filter(is_read=False).count()

    # 获取用户参与的课程数量
    # print('-' * 50, user)
    st=Student()
    st.phone=user.phone
    st.notes=user.notes
    st.programming_level=user.programming_level

    course_count = CourseEnrollment.objects.filter(student=st).count()

    # 获取下节课信息（假设按照课程开始时间排序取最近的一门课程）
    now = datetime.datetime.now()
    enrollments = CourseEnrollment.objects.filter(student=st)
    next_course = None
    for enrollment in enrollments:
        if enrollment.start_date >= now:
            next_course = enrollment.course
            break

    next_course_datetime = None
    next_course_name = None
    if next_course:
        next_course_datetime = next_course.start_date
        next_course_name = next_course.name

    # 获取用户可预订的课程列表（假设根据用户的编程水平等条件筛选）
    available_courses = []
    if user.is_student:
        student_level = user.student.programming_level
        available_tutors = Tutor.objects.filter(is_available=True)
        for tutor  in available_tutors:
            for course in tutor.courses.all():
                if course.language == student_level:
                    available_courses.append(course)

    # 获取用户的发票信息
    invoices = Invoice.objects.filter(student=st)

    context = {
        'user': user,
        #'unread_notifications_count': unread_notifications_count,
        'course_count': course_count,
        'next_course_datetime': next_course_datetime,
        'next_course_name': next_course_name,
        'available_courses': available_courses,
        'invoices': invoices
    }

    return render(request, 'dashboard.html', context)

@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is connected."""
    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
                )
        else:
            return self.redirect_when_logged_in_url



class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


# class LogInView(LoginProhibitedMixin, View):
#     """Display login screen and handle user login."""
#     http_method_names = ['get', 'post']
#     redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN
#
#     def get(self, request):
#         """Display log in template with an empty login form."""
#         next_url = request.GET.get('next') or ''
#         form = AuthenticationForm()
#         return render(request, 'log_in.html', {'form': form, 'next': next_url})
#
#     def post(self, request):
#         """Handle log in attempt."""
#         form = AuthenticationForm(request, data=request.POST)
#         next_url = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(next_url)
#             else:
#                 messages.add_message(request, messages.ERROR, "用户名或密码错误，请重新输入。")
#         else:
#             messages.add_message(request, messages.ERROR, "请检查输入的用户名和密码是否正确。")
#
#         return render(request, 'log_in.html', {'form': form, 'next': next_url})

def log_out(request):
    """Log out the current user"""
    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
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
        # 这里修正了一个错误，应该是重新登录当前用户
        login(request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""
        messages.add_message(request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""
    # 这里修正了一个错误，model应该是User而不是UserForm
    model = User
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""
    # 这里修正了一个错误，form_class应该是SignUpForm而不是SignUpView
    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


def course_booking_view(request):
    """
    处理课程预订的视图函数。

    这里可以实现诸如获取可预订课程列表、处理学生预订请求、验证预订条件等功能。
    """
    if request.method == 'POST':
        # 处理POST请求，比如获取学生提交的预订信息
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')

        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        # 这里可以添加更多的预订条件验证逻辑，比如检查学生是否已经预订过该课程、课程是否还有名额等

        # 如果验证通过，执行预订操作，比如创建一个课程预订记录（假设已经有相关的课程预订模型类定义）
        # booking = CourseBooking.objects.create(student=student, course=course)

        return redirect('success_page')  # 预订成功后重定向到成功页面，这里的'success_page'需要根据实际项目中定义的URL名称来替换

    else:
        # 处理GET请求，比如获取可预订课程列表并传递给模板进行展示
        available_courses = Course.objects.filter(is_available=True)  # 假设课程模型类中有is_available字段来表示是否可预订

        context = {
            'available_courses': available_courses
        }

        return render(request, 'course_booking.html', context)

def invoice_view(request):
    """
    处理发票相关操作的视图函数，比如生成发票、查看发票详情等。

    这里可以实现诸如获取特定学生的发票信息、根据订单生成新发票、展示发票详细内容等功能。
    """
    if request.method == 'POST':
        # 处理POST请求，例如根据学生订单信息生成发票
        student_id = request.POST.get('student_id')
        student = Student.objects.get(id=student_id)

        # 假设这里有相关业务逻辑来生成发票，比如根据学生的课程消费记录等生成新的Invoice实例
        # invoice = Invoice.objects.create(student=student, amount=total_amount, status='Unpaid', due_date=due_date)

        return redirect('invoice_success_page')  # 生成发票成功后重定向到成功页面，这里的'invoice_success_page'需根据实际项目中定义的URL名称来替换

    else:
        # 处理GET请求，比如获取并展示特定学生的发票信息
        student_id = request.GET.get('student_id')
        student = Student.objects.get(id=student_id)

        invoices = Invoice.objects.filter(student=student)

        context = {
            'student': student,
            'invoices': invoices
        }

        return render(request, 'invoice.html', context)

class StudentListView(ListView):
    model = Student
    template_name ='student_list.html'
    context_object_name ='students'

    def get_queryset(self):
        return super().get_queryset().order_by('user__last_name')