from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import CustomUser as User
from .models import Host

@receiver(post_save, sender=User)
def create_host_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_host:
            Host.objects.create(user=instance)

@receiver(pre_delete, sender=Host)
def delete_host_profile(sender, instance, using, **kwargs):
    instance.user.is_host = False
