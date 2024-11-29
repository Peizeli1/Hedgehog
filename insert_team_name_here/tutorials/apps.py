from django.apps import AppConfig


class TutorialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorials'

    def ready(self):
        # Explicitly importing key modules within the application ensures that they are loaded correctly when the application is launched.
        from. import views
        from. import models
        from. import forms
