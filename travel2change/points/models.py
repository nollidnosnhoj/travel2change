from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PointValue(models.Model):
    key = models.CharField(_('key'), max_length=50, help_text=_('Choose a key name of this point value'))
    value = models.IntegerField(_('value'), blank=False, default=0)

    def __str__(self):
        return "{0} points for {1}.".format(self.value, self.key)


class AwardedPoint(models.Model):
    target = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=_('awardedpoint_target'))
    point_value = models.ForeignKey(PointValue, blank=True, null=True, on_delete=models.CASCADE)
    reason = models.CharField(_('reason'), max_length=255, blank=True)
    points = models.IntegerField(_('points'), default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        val = self.point_value
        if self.point_value is None:
            val = "{0} points".format(self.points)
        return "{0} awarded to {1}.".format(val, self.target)
    
    def save(self, *args, **kwargs):
        if self.point_value:
            self.points = self.point_value.value
        super().save(*args, **kwargs)


def get_points(key):
    point_value = None
    if isinstance(key, int) and not isinstance(key, bool):
        points = key
    else:
        try:
            point_value = PointValue.objects.get(key=key)
            points = point_value.value
        except PointValue.DoesNotExist:
            points = 0
    return point_value, points


def award_points(target, key, reason=""):
    """
    This is a helper function for awarding points to a user.
    The key param can either be a int or string. Int will convert the key to points.
    String will get the PointValue object based on the key value.
    
    Parameters:
        target (User) - The user instance that will be awarded points
        key (int or string) - Determine the amount of points the user will be awarded.
        reason (string) - Reasons to award user instance
    """
    point_value, points = get_points(key)
    award_points = AwardedPoint(points=points, point_value=point_value, reason=reason)
    if isinstance(target, get_user_model()):
        award_points.target = target
    else:
        raise ImproperlyConfigured('target param in award_points function needs to be a user model')
    award_points.save()
    return award_points


def unaward_points(target, key):
    """
    This will undo the award_points function (delete the AwardedPoint object) and update the user's points

    Parameters:
        target (User instance) - The user that will be unawarded.
        key (int or string) - Find the amount of points to undo.
    """
    point_value, points = get_points(key)
    try:
        award_points = AwardedPoint.objects.get(target=target, point_value=point_value, points=points)
    except AwardedPoint.DoesNotExist:
        return
    award_points.delete()
    return award_points
