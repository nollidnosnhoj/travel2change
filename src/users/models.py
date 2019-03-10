from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(_('email address'), unique=True)
    first_name      = models.CharField(_('first name'), max_length=60, blank=False, null=False)
    last_name       = models.CharField(_('last name'), max_length=60, blank=False, null=False)
    date_joined     = models.DateTimeField(default=timezone.now)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_host         = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


"""
from activities.models import Activity, Tag


class UserSettings(models.Model):
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    interests       = models.ManyToManyField(
                        Tag, related_name=_('interest'),
                        help_text=_('What type(s) of activities are you interested in?'),
                    )
    bookmarks       = models.ManyToManyField(Activity, related_name=_('bookmarked'))

    def __str__(self):
        return self.user.email
"""
