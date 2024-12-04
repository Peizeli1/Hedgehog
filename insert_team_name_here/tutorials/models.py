from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from. import utils


class User(AbstractUser):
    """
    自定义用户模型类，继承自AbstractUser，添加了额外的字段和功能。

    这个类扩展了Django默认的用户模型，以满足特定项目的需求，例如区分不同角色的用户（学生、导师、管理员）等。
    """

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'tutor'),
        ('admin', 'admin'),
    ]

    # 用户名验证器，确保用户名符合特定格式要求
    username_validator = RegexValidator(
        regex=r'^@[a-zA-Z0-9]{3,}$',
        message='用户名必须由@开头，后面跟着至少三个字母数字字符，且除@外不能有其他特殊字符'
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='student',
        help_text="定义用户的角色（学生、导师或管理员）。"
    )

    class Meta:
        """
        模型类的元数据选项。

        这里定义了模型类的一些额外属性，如默认的排序方式等。
        """
        ordering = ['last_name', 'first_name']

    def full_name(self):
        """
        返回包含用户全名的字符串。

        将用户的姓和名拼接成一个完整的姓名字符串。
        """
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """
        使用工具函数返回用户的Gravatar头像链接。

        :param size: 头像的尺寸大小，默认值为120像素。
        :return: 用户Gravatar头像的链接字符串。
        """
        return utils.get_gravatar_url(self.email, size)

    def mini_gravatar(self):
        """
        使用工具函数返回用户的微型Gravatar头像链接。

        :return: 用户微型Gravatar头像的链接字符串。
        """
        return utils.get_mini_gravatar_url(self.email)

    def __str__(self):
        """
        用户对象的字符串表示形式。

        返回一个包含用户全名、用户名以及角色显示名称的字符串，以便在需要显示用户信息的地方能够清晰展示。
        """
        return f"{self.full_name()} (@{self.username}) - {self.get_role_display()}"


class Student(models.Model):
    """
    与用户关联的学生特定数据模型类。

    每个学生对象都与一个用户对象相关联，并存储了学生特有的信息，如电话号码、备注信息、编程水平等。
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    phone_validator = RegexValidator(
        regex=r'^[0-9 -]+$',
        message='电话号码应只包含数字、空格和连字符'
    )
    phone = models.CharField(max_length=20, validators=[phone_validator])
    notes = models.TextField(blank=True, null=True)
    programming_level = models.CharField(max_length=50, choices=[('初学者', '初学者'), ('中级', '中级'),
                                                                 ('高级', '高级')], default='初学者',
                                         help_text="学生的编程水平。")

    def __str__(self):
        """
        学生对象的字符串表示形式。

        返回与该学生关联的用户的全名，以便在需要显示学生信息的地方能够清晰展示。
        """
        return self.user.full_name()


class CourseType(models.Model):
    """
    定义代码辅导项目所提供的课程类型模型类。

    用于存储不同课程类型的相关信息，如课程名称、描述、所需技能水平等。
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text="课程名称，例如：使用Ruby on Rails进行Web开发。")
    description = models.TextField(help_text="课程的详细描述。")
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('初学者', '初学者'),
            ('中级', '中级'),
            ('高级', '高级'),
        ],
        default='初学者',
        help_text="课程所需的技能水平。"
    )

    def __str__(self):
        """
        课程类型对象的字符串表示形式。

        返回课程类型的名称，以便在需要显示课程类型信息的地方能够清晰展示。
        """
        return self.name


class Tutor(models.Model):
    """
    与用户关联的导师特定数据模型类。

    每个导师对象都与一个用户对象相关联，并存储了导师特有的信息，如专业领域、是否可授课状态、能教授的高级课程等。
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tutor'})
    expertise = models.CharField(max_length=255, help_text="例如：Python、Java")
    is_available = models.BooleanField(default=True, help_text="表示导师是否可授课的状态。")
    advanced_courses = models.ManyToManyField(
        CourseType,
        blank=True,
        help_text="导师能教授的高级课程列表。"
    )

    def __str__(self):
        """
        导师对象的字符串表示形式。

        返回与该导师关联的用户的全名，以便在需要显示导师信息的地方能够清晰展示。
    """
        return self.user.full_name()


class Course(models.Model):
    """
    课程模型类，用于表示学生和导师之间安排的课程。

    存储了课程的相关信息，如参与的学生、导师、课程类型、上课时间、时长、地点、状态等。
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='courses_enrolled'  # 反向查询时，学生可以通过这个名称获取自己参与的所有课程
    )
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='courses_taught'  # 反向查询时，导师可以通过这个名称获取自己教授的所有课程
    )
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        related_name='courses_offered',  # 反向查询时，课程类型可以通过这个名称获取所有基于该类型的课程
        help_text="所教授课程的类型。"
    )
    day_of_week = models.CharField(max_length=10, help_text="例如：星期一、星期二")
    time_slot = models.TimeField()
    duration = models.IntegerField(help_text="时长（以分钟为单位）。")
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="已安排", help_text="例如：已安排、已取消。")

    def __str__(
        self):
        """
        课程对象的字符串表示形式。

        返回一个包含学生全名、导师全名以及课程类型名称的字符串，以便在需要显示课程信息的地方能够清晰展示。
        """
        return f"{self.student.user.full_name()} - {self.tutor.user.full_name()} ({self.course_type.name})"


class Invoice(models.Model):
    """
    发票模型类，用于跟踪学生的计费信息。

    存储了与发票相关的信息，如关联的学生、金额、状态、到期日期等。
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="未支付", help_text="例如：已支付、未支付。")
    due_date =models.DateField()

    def __str__(self):
        """
        发票对象的字符串表示形式。

        返回一个包含发票编号、学生全名、金额、到期日期以及状态的字符串，以便在需要显示发票信息的地方能够清晰展示。
        """
        return f"发票 {self.id}: {self.student.user.full_name()} - 金额: {self.amount}, 到期日期: {self.due_date}, 状态: {self.status}"


class CourseEnrollment(models.Model):
    """
    课程注册模型类，用于记录学生对课程的注册信息。

    存储了学生注册课程的相关信息，如注册的学生、课程、注册日期、是否处于活动状态等，并提供了一些操作注册状态的方法。
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="表示该课程注册是否处于活动状态。")

    def __str__(self):
        """
        课程注册对象的字符串表示形式。

        返回一个包含学生全名、课程名称、注册时间以及状态的字符串，以便在需要显示课程注册信息的地方能够清晰展示。
        """
        return f"{self.student.user.full_name()} - {self.course.name} (注册时间: {self.enrollment_date}, 状态: {'活动' if self.is_active else '非活动'})"

    def cancel_enrollment(self):
        """
        取消当前课程注册记录，将其设置为非活动状态。

        更改课程注册记录的 `is_active` 属性为 `False`，并保存到数据库。
        """
        self.is_active = False
        self.save()

    def reactivate_enrollment(self):
        """
        重新激活当前课程注册记录，将其设置为活动状态。

        更改课程注册记录的 `is_active` 属性为 `True`，并保存到数据库。
        """
        self.is_active = True
        self.save()

    def is_enrolled(self, student, course):
        """
        检查指定学生是否已经注册了指定课程。

        :param student: 要检查的学生对象
        :param course: 要检查的课程对象
        :return: True 如果学生已经注册了该课程，否则 False
        """
        return CourseEnrollment.objects.filter(student=student, course=course, is_active=True).exists()


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', '待处理'), ('Confirmed', '已确认'), ('Cancelled', '已取消')])

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} ({self.status})"