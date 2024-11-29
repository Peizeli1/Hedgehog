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

    # 首页路由，访问根路径时展示应用的起始页面

    # 用户仪表盘路由，展示用户相关的各种信息和操作入口
    path('dashboard/', views.dashboard, name='dashboard'),

    # 登录路由，处理用户登录请求并展示登录页面
    path('log_in/', views.LogInView.as_view(), name='log_in'),

    # 登出路由，处理用户登出操作
    path('log_out/', views.log_out, name='log_out'),

    # 修改密码路由，引导用户修改密码并处理相关请求
    path('password/', views.PasswordView.as_view(), name='password'),

    # 用户资料更新路由，用于用户更新个人资料信息
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

    # 用户注册路由，展示注册页面并处理新用户注册请求
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    # 课程预订相关路由（假设你在视图函数中实现了课程预订相关视图，如course_booking_view等）
    path('course_booking/', views.course_booking_view, name='course_booking'),

    # 发票相关路由（假设你在视图函数中实现了查看发票、支付发票等相关视图）
    path('invoice/', views.invoice_view, name='invoice'),

    # 如果有其他应用需要集成到当前项目，可通过include函数引入其URL配置
    # 例如，如果有一个名为'blog'的应用，其有自己的urls.py文件，可以这样引入：
    # path('blog/', include('blog.urls'))

]

# 处理静态文件的路由配置，确保在开发环境下能正确加载静态文件（如CSS、JavaScript、图片等）
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 如果在项目中使用了媒体文件（如用户上传的文件等），还需要添加以下配置来处理媒体文件的路由
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)