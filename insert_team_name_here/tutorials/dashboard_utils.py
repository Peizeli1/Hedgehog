import datetime
from.models import User, CourseEnrollment, Invoice, Tutor, Student


def get_user_data(user):
    """获取用户相关数据的函数"""
    unread_notifications_count = user.notifications.filter(is_read=False).count()
    course_count = CourseEnrollment.objects.filter(student=user).count()

    now = datetime.datetime.now()
    enrollments = CourseEnrollment.objects.filter(student=user)
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

    return {
        'unread_notifications_count': unread_notifications_count,
        'course_count': course_count,
        'next_course_datetime': next_course_datetime,
        'next_course_name': next_course_name
    }


def get_available_courses(user):
    """获取用户可预订的课程列表的函数"""
    available_courses = []
    if user.is_student:
        student_level = user.student.programming_level
        available_tutors = Tutor.objects.filter(is_available=True)
        for tutor in available_tutors:
            for course in tutor.courses.all():
                if course.language == student_level:
                    available_courses.append(course)

    return available_courses


def get_user_invoices(user):
    """获取用户的发票信息的函数"""
    return Invoice.objects.filter(student=user)