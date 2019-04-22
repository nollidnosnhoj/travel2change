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


class AwardedPoints(models.Model):
    target = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=_('awarded_points'))
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
        self.target.update_points(self.points)
        super().save(*args, **kwargs)


def award_points(target, key, reason=""):
    point_value = None
    if isinstance(key, int) and not isinstance(key, bool):
        points = key
    else:
        try:
            point_value = PointValue.objects.get(key=key)
            points = point_value.value
        except PointValue.DoesNotExist:
            raise ImproperlyConfigured('PointValue for {0} does not exist'.format(key))
    award_points = AwardedPoints(points=points, point_value=point_value, reason=reason)
    if isinstance(target, get_user_model()):
        award_points.target = target
    else:
        raise ImproperlyConfigured('target param in award_points function needs to be a user model')
    award_points.save()
    return award_points
