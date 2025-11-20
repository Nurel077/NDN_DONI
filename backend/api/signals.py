from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserSettings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создать профиль и настройки при создании пользователя"""
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserSettings.objects.get_or_create(user=instance)

