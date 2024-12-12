from django.urls import path
from . import views

app_name = 'tutorials'

urlpatterns = [
    # Home and Dashboard
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # User Authentication
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.LogOutView.as_view(), name='log_out'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('mark_as_read/<int:notification_id>/', views.NotificationsView.as_view(), name='mark_as_read'),
    # Profile Management
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_update'),

    # Course Management
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('course_booking/', views.CourseBookingView.as_view(), name='course_booking'),
    path('course_booking/confirm/<int:course_id>/', views.CourseBookingConfirmView.as_view(), name='course_booking_confirm'),
    path('tutors/', views.TutorListView.as_view(), name='tutor_list'), 

    # Invoice Management
    path('invoice/', views.InvoiceView.as_view(), name='invoice'),
    
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
]
