from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Host
from users.models import CustomUser as User


"""
This function will create a Host profile if the user
instance is created.
"""
@receiver(post_save, sender=User)
def create_host_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_host:
            Host.objects.create(user=instance)


"""
This function will set the host status in user's account to False 
before deleting Host profile database.
"""
@receiver(pre_delete, sender=Host)
def remove_host_status(sender, instance, using, **kwargs):
    user = instance.user
    user.is_host = False
    user.save()
