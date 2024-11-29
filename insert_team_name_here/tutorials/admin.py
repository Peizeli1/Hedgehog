from django.contrib import admin

#reigister your model here

# from.models import User, Course, CourseEnrollment, Invoice, Tutor, Student
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_student', 'is_tutor', 'date_joined')
#     list_filter = ('is_student', 'is_tutor')
#     search_fields = ('username', 'email')
#
#     # 假设你的User模型中有如下相关字段定义（请根据实际情况调整）
#     def is_student(self, obj):
#         return obj.role =='student'
#
#     def is_tutor(self, obj):
#         return obj.role == 'tutor'
#
#     is_student.short_description = '是否为学生'
#     is_tutor.short_description = '是否为导师'
#
#
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'tutor', 'cost', 'is_available')
#     list_filter = ('tutor', 'is_available')
#     search_fields = ('name',)
#
#     # 假设你的Course模型中有如下相关字段定义（请根据实际情况调整）
#     def name(self, obj):
#         return obj.course_type.name
#
#     def tutor(self, obj):
#         return obj.tutor.user.full_name()
#
#     def cost(self, obj):
#         return obj.course_type.price  # 假设CourseType模型中有price字段，用于表示课程价格，你可根据实际情况调整
#
#     def is_available(self, obj):
#         return obj.is_available  # 假设Course模型中有is_available字段用于表示课程是否可预订等情况，你可根据实际情况调整
#
#     name.short_description = '课程名称'
#     tutor.short_description = '授课导师'
#     cost.short_description = '课程价格'
#     is_available.short_description = '是否可预订'
#
#
# class CourseEnrollmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'course','start_date', 'end_date')
#     list_filter = ('student', 'course')
#
#     # 假设你的CourseEnrollment模型中有如下相关字段定义（请根据实际情况调整）
#     def student(self, obj):
#         return obj.student.user.full_name()
#
#     def course(self, obj):
#         return obj.course.name
#
#     def start_date(self, obj):
#         return obj.start_time  # 假设CourseEnrollment模型中有start_time字段表示开始时间，你可根据实际情况调整
#
#     def end_date(self, obj):
#         return obj.end_time  # 假设CourseEnrollment模型中有end_time字段表示结束时间，你可根据实际情况调整
#
#     student.short_description = '学生姓名'
#     course.short_description = '课程名称'
#     start_date.short_description = '开始时间'
#     end_date.short_description = '结束时间'
#
#
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'amount', 'due_date', 'payment_status')
#     list_filter = ('student', 'payment_status')
#     search_fields = ('student',)
#     # 假设你的Invoice模型中有如下相关字段定义（请根据实际情况调整）
#     def student(self, obj):
#         return obj.student.user.full_name()
#
#     def payment_status(self, obj):
#         return obj.status
#
#     student.short_description = '学生姓名'
#     payment_status.short_description = '支付状态'
#
#
# class TutorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_available')
#     list_filter = ('is_available',)
#     search_fields = ('user',)
#     # 假设你的Tutor模型中有如下相关字段定义（请根据实际情况调整）
#     #def user(self, img src="/Users/lipeize/Desktop/Hedgehog/venv/Hedgehog/insert_team_name_here/tutorials/models.py changed, reloading." width="100%")
#         #return img.src.full_name()
#
#     def is_available(self, obj):
#         return obj.is_available  # 假设Tutor模型中有is_available字段用于表示导师是否可授课等情况，你可根据实际情况调整
#
#     User.short_description = '导师姓名'
#     is_available.short_description = '是否可授课'
#
#
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'programming_level')
#
#     # 假设你的Student模型中有如下相关字段定义（请根据实际情况调整）
#     def user(self, obj):
#         return obj.user.full_name()
#
#     user.short_description = '学生姓名'
#
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
# admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(Tutor, TutorAdmin)
# admin.site.register(Student, StudentAdmin)