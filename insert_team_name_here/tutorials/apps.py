from django.apps import AppConfig


class TutorialsConfig(AppConfig):
    """
    Application configuration for the 'tutorials' app.
    This handles app initialization routines, such as registering signals.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorials'

    def ready(self):
        """
        Load signals and other startup routines required for the application.
        This method is executed when the app is initialized.
        """
        print("TutorialsConfig ready: App initialization started.")
        try:
            import tutorials.signals  # Register signals for the app
        except ImportError as e:
            raise ImportError(
                f"Failed to import 'tutorials.signals'. Ensure the file exists and is error-free. Details: {e}"
            )
