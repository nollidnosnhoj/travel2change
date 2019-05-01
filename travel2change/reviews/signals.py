from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from points.models import award_points, unaward_points
from .models import Review

@receiver(post_save, sender=Review)
def award_points_for_review(sender, instance, created, **kwargs):
    """ Award points when a review is created """
    if created:
        award_points(instance.user, 'review_create')
        # if the review has a photo when created, award points
        if instance.photo:
            award_points(instance.user, 'review_photo')


@receiver(pre_delete, sender=Review)
def unaward_points_for_review(sender, instance, using, **kwargs):
    """ Unaward points when a review is deleted """
    unaward_points(instance.user, 'review_create')
