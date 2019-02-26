from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=60, blank=False)
    image = models.ImageField(upload_to='region')
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    font_awesome = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.name

class Activity(models.Model):
    host            = models.ForeignKey(User, related_name=_("host"), on_delete=models.CASCADE)
    title           = models.CharField(verbose_name=_("title"), max_length=255, blank=False)
    slug            = models.SlugField(max_length=255, unique=True)
    description     = models.TextField(verbose_name=_("description"), max_length=400)
    highlights      = models.TextField(verbose_name=_("highlights"), max_length=400)
    requirements    = models.TextField(verbose_name=_("requirements"), max_length=400, blank=True)
    region          = models.ForeignKey(Region, verbose_name=_("region"), on_delete=models.CASCADE)
    tags            = models.ManyToManyField(Tag, verbose_name=_("tags"), blank=True)
    address         = models.CharField(verbose_name=_("address"), max_length=255, blank=False)
    latitude        = models.DecimalField(verbose_name=_("latitude"), max_digits=9, decimal_places=6)
    longitude       = models.DecimalField(verbose_name=_("longitude"), max_digits=9, decimal_places=6)
    price           = models.DecimalField(verbose_name=_("price"), max_digits=6, decimal_places=2)

    review_count    = models.IntegerField(blank=True, default=0, verbose_name=_("review count"))

    created         = models.DateTimeField(auto_now_add=True, verbose_name=_("activity created date"))

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, related_name='images', on_delete=models.CASCADE)
    caption = models.CharField(max_length=60)
    image = models.ImageField(upload_to='activity_images/', blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
