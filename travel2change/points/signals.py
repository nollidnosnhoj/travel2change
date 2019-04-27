from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AwardedPoint

User = get_user_model()

# signal is called when an awardedpoint object is saved
@receiver(post_save, sender=AwardedPoint)
def add_points(sender, instance, created, **kwargs):
    instance.target.update_points(instance.points)

# signal is called when an awardedpoint object is deleted
@receiver(pre_delete, sender=AwardedPoint)
def remove_points(sender, instance, using, **kwargs):
    removed_points = -1 * (instance.points)
    instance.target.update_points(removed_points)
