from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from activities.models import Activity

User = get_user_model()


def get_review_image_filename(instance, filename):
    return 'uploads/reviews/user-{0}/activity-{1}/review-{2}/{3}'.format(instance.user.pk, instance.activity.pk, instance.pk, filename)

class Review(models.Model):
    RATING_CHOICES  = (
        (1, 'Terrible'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Very Good'),
        (5, 'Exceptional'),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    activity        = models.ForeignKey(
                        Activity,
                        on_delete=models.CASCADE,
                        related_name=_('reviews')
                    )
    content         = models.TextField(_('content'), blank=False)
    rating          = models.IntegerField(choices=RATING_CHOICES)
    photo           = models.ImageField(
                        _('review photo'),
                        upload_to=get_review_image_filename,
                        blank=True,
                        null=True,
                    )

    show_name       = models.BooleanField(default=False,
                        help_text=_('Show your name in public. You can see still your name, regardless if checked or not.'))
    show_email      = models.BooleanField(default=False,
                        help_text=_('Email will only show for the host of the activity.'))

    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)

    objects         = models.Manager()

    class Meta:
        unique_together = (('user', 'activity', ))
        ordering = ('created', )
    
    def __str__(self):
        return 'Review by {0} on {1}'.format(self.user, self.activity)
