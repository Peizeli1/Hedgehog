from django.contrib import admin
from .models import User, Student, Tutor, Course, CourseType, CourseEnrollment, Invoice


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model."""
    list_display = ('username', 'email', 'role', 'date_joined')
    list_filter = ('role',)
    search_fields = ('username', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for Student model."""
    list_display = ('user', 'programming_level')
    search_fields = ('user__username', 'user__email')


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Admin configuration for Tutor model."""
    list_display = ('user', 'expertise', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('user__username', 'user__email')


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    """Admin configuration for CourseType model."""
    list_display = ('name', 'skill_level')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model."""
    list_display = ('course_type', 'tutor', 'day_of_week', 'status')
    list_filter = ('status', 'day_of_week')
    search_fields = ('course_type__name', 'tutor__user__username')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for CourseEnrollment model."""
    list_display = ('student', 'course', 'status', 'enrollment_date')
    list_filter = ('status',)
    search_fields = ('student__user__username', 'course__course_type__name')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Invoice model."""
    list_display = ('student', 'amount', 'status', 'due_date')
    list_filter = ('status',)
    search_fields = ('student__user__username',)
