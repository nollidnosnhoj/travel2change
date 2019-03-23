from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.fields import AutoSlugField
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(_('email address'), unique=True)
    first_name      = models.CharField(_('first name'), max_length=60, blank=False, null=False)
    last_name       = models.CharField(_('last name'), max_length=60, blank=False, null=False)
    date_joined     = models.DateTimeField(default=timezone.now)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Host(models.Model):
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    _name           = models.CharField(
                        _('name'),
                        max_length=60,
                        blank=True,
                        help_text=_("Provide a name of your organization. This will also be in your profile's URL.\n"
                                    "Ex. travel2change.org/hosts/your-organization-name"),
                    )
    slug           = AutoSlugField(
                        populate_from=['name'],
                        overwrite=True
                    )
    description     = models.TextField(
                        _('description'),
                        max_length=400,
                        blank=True,
                        help_text=_('Tell us about you or your organization.'),
                    )
    phone           = PhoneNumberField(
                        _('phone'),
                        blank=True,
                        help_text=_('Provide a contact phone number in +12223334444.')
                    )
    website         = models.URLField(
                        _('website'),
                        blank=True,
                        help_text=_("Provide a link to your website.")
                    )

    """
    If host has a host name, then the activities and profile will display the host name,
    or else it will display the user's full name
    """
    @property
    def name(self):
        if self._name:
            return self._name
        return self.user.get_full_name()

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('host_detail', kwargs={'slug': self.slug})
