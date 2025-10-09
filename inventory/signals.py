from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Notification, Profile, InventoryItem, InventoryChange


# Signal to create or update user profile when a User instance is created or updated
@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=InventoryItem)
def create_initial_inventory_change(sender, instance, created, **kwargs):
    if created and instance.quantity > 0:
        InventoryChange.objects.create(
            item=instance,
            user=instance.user,  # user can be null if created by admin
            change_type='RESTOCK',
            quantity_change=instance.quantity,
            previous_quantity=0,
            new_quantity=instance.quantity,
            reason='Initial stock entry',
        )