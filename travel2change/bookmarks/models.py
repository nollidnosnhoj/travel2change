from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from activities.models import Activity

User = get_user_model()

class Bookmark(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_('bookmarks'))
    activity    = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=True)

    objects     = models.Manager()

    def __str__(self):
        return '{0} bookmarked {1}'.format(self.user.get_full_name(), self.activity.title)
