from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that takes an email address as the username field.
    """
    email           = models.EmailField(_('email address'), unique=True)
    first_name      = models.CharField(_('first name'), max_length=60, blank=False, null=False)
    last_name       = models.CharField(_('last name'), max_length=60, blank=False, null=False)
    date_joined     = models.DateTimeField(default=timezone.now)
    is_active       = models.BooleanField(
                        _('Active'),
                        default=True,
                        help_text=_('Designates whether this user account should be considered active.'),
                    )
    is_staff        = models.BooleanField(
                        _('Staff'),
                        default=False,
                        help_text=_('Designates whether this user can access the admin site.'),
                    )
    is_superuser    = models.BooleanField(
                        _('Superuser'),
                        default=False,
                        help_text=_('Designates that this user has all permissions without explicitly assigning them.'),
                    )

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
    
    @property
    def full_name(self):
        return self.get_full_name()


class Host(models.Model):
    """
    This host object will create a profile for the user. This will also grant user host permissions.
    """
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    _name           = models.CharField(
                        _('name'),
                        max_length=60,
                        blank=True,
                        help_text=_("Provide a name of your organization. This will also be in your profile's URL.\n"
                                    "Ex. travel2change.org/hosts/your-organization-name"),
                    )
    slug            = AutoSlugField(
                        populate_from='profile_slug',
                        always_update=True,
                        unique=True,
                    )
    custom_slug     = models.SlugField(
                        _('custom slug'),
                        max_length=50,
                        blank=True,
                        help_text=_('Create a custom slug for your profile. Example: travel2change.org/hosts/your-custom-slug'),
                    )
    description     = models.TextField(
                        _('description'),
                        max_length=400,
                        blank=True,
                        help_text=_('Tell us about you or your organization.'),
                    )
    contact_email   = models.EmailField(
                        _('contact email'),
                        max_length=255,
                        blank=True,
                        help_text=_('Enter an email address that you like visitors to contact.')
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
    fh_username     = models.CharField(
                        _('fareharbor username'),
                        max_length=60,
                        blank=True,
                        default=_('travel2change'),
                        help_text=_('Enter your FareHarbor username. This is required if you are hosting paid activities')
                    )

    @property
    def name(self):
        """
        If host name is defined, use it as the host name.
        If not, use the user's full name.
        """
        return self._name if self._name else self.user.full_name

    @property
    def profile_slug(self):
        """
        If custom slug is defined, use it as slug.
        If not, use the host's name.
        """
        return self.custom_slug if self.custom_slug else self.name
    
    @property
    def get_fh_username(self):
        """
        If the fareharbor username is not present, default to 'travel2change'
        """
        if self.fh_username is None or self.fh_username == "":
            return _('travel2change')
        return self.fh_username

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('host_detail', kwargs={'slug': self.slug})
