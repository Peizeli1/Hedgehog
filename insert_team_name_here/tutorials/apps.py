from django.apps import AppConfig


class TutorialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorials'

    def ready(self):
        # 显式导入应用内的关键模块，确保在应用启动时它们被正确加载
        from. import views
        from. import models
        from. import forms