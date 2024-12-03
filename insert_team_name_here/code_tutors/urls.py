"""
URL configuration for code_tutors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from tutorials.views import StudentListView, course_booking_view, dashboard
from tutorials import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('students', views.StudentListView.as_view(), name='student_list'),

    # First page routing, show application's start page when accessing the root path

    # User dashboard routing, displaying various information related to the user and the operation portal
    path('dashboard/', views.dashboard, name='dashboard'),

    # Login route that handles user login requests and displays the login page
    path('log_in/', views.LogInView.as_view(), name='log_in'),

    # Logout routing to handle user logout operations
    path('log_out/', views.log_out, name='log_out'),

    # Change password routing, guiding users to change their passwords and handling related requests
    path('password/', views.PasswordView.as_view(), name='password'),

    # User Profile Update Route for users to update their profile information
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

    # User registration route to display the registration page and handle new user registration requests
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    # Course booking related routes (assuming you have implemented course booking related views in view functions such as course_booking_view and other user registration routes to display the registration page and handle new user registration requests）
    path('course_booking/', views.course_booking_view, name='course_booking'),

    # Invoice related routing (assuming you have implemented views related to viewing invoices, paying invoices, etc. in view functions）
    path('invoice/', views.invoice_view, name='invoice'),

    path('tutors/', views.TutorsView.as_view(), name='tutors'),

    path('tutors_invoices/', views.InvoicesTutors.as_view(), name='tutors_invoices'),

    path('tutors_calendar/', views.CalendarView.as_view(), name='tutors_calendar'),

    # If there are other applications that need to be integrated into the current project, their URL configuration can be introduced via the include function.
    # For example, if there is an application named 'blog' that has its own urls.py file, it can be introduced like this:
    # path('blog/', include('blog.urls'))

]

# Handle the routing configuration of static files to ensure that static files (e.g. CSS, JavaScript, images, etc.) are loaded correctly in the development environment
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# If you are using media files in your project (e.g., user uploaded files, etc.), you will also need to add the following configuration to handle the routing of media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
