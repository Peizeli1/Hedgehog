from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student, Tutor

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Student or Tutor profile when a User is created.
    """
    if created:
        try:
            if instance.role == 'student':
                Student.objects.create(user=instance)
            elif instance.role == 'tutor':
                Tutor.objects.create(user=instance)
        except Exception as e:
            # Log or print the exception for debugging
            print(f"Error creating profile for user {instance}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically save the associated profile when a User is saved.
    """
    try:
        if instance.role == 'student' and hasattr(instance, 'student'):
            instance.student.save()
        elif instance.role == 'tutor' and hasattr(instance, 'tutor'):
            instance.tutor.save()
    except Exception as e:
        # Log or print the exception for debugging
        print(f"Error saving profile for user {instance}: {e}")
