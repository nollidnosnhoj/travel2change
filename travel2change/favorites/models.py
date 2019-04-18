from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from activities.models import Activity

User = get_user_model()

class Favorite(models.Model):
    user        = models.ForeignKey(User, db_index=False, on_delete=models.CASCADE, related_name=_('favorites'), blank=False)
    activity    = models.ForeignKey(Activity, db_index=False, on_delete=models.CASCADE, blank=False)
    created     = models.DateTimeField(auto_now_add=True)

    objects     = models.Manager()

    class Meta:
        unique_together = (('user', 'activity', ))

    def __str__(self):
        return '{0} favorited {1}'.format(self.user.get_full_name(), self.activity.title)
