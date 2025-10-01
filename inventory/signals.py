from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile


# Signal to create or update user profile when a User instance is created or updated
@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()