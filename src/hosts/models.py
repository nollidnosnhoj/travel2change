from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import ugettext as _

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Host(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    _name            = models.CharField(_('name'),
                        max_length=60,
                        blank=True,
                        help_text=_('Your name or organization. Will be displayed on your profile and activities.'),
                    )
    description     = models.TextField(_('description'), max_length=400, blank=True,
                        help_text=_('Tell us about you or your organization.'),
                    )
    phone           = PhoneNumberField(_('phone'), blank=True, help_text=_('Contact phone number'))
    website         = models.URLField(_('website'), blank=True, help_text=_("Your or organization's website"))

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('hosts:detail', kwargs={'pk': self.pk})

    """
    If host has a host name, then the activities and profile will display the host name,
    or else it will display the user's full name
    """
    @property
    def name(self):
        if self._name:
            return self._name
        return self.user.get_full_name()
