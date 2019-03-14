import itertools
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from .managers import ActivityManager
from hosts.models import Host


class Region(models.Model):
    name = models.CharField(max_length=60, blank=False)

    objects = models.Manager()
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    font_awesome = models.CharField(max_length=60, blank=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Activity(models.Model):
    host            = models.ForeignKey(
                        Host,
                        related_name=_("host"),
                        on_delete=models.CASCADE
                    )
    title           = models.CharField(
                        verbose_name=_("title"),
                        max_length=255,
                        blank=False,
                        null=False,
                        help_text=_("Insert a name for your activity"),
                    )
    slug            = models.SlugField(max_length=255, unique=True)
    description     = models.TextField(
                        verbose_name=_("description"),
                        max_length=400,
                        help_text=_("Describe the activity. (Max. 400 characters)")
                    )
    highlights      = models.TextField(
                        verbose_name=_("highlights"),
                        max_length=400,
                        help_text=_("List what makes this activity unique. (Max. 400 characters) "
                                    "\nPlease insert each highlight per line.")
                    )
    requirements    = models.TextField(
                        verbose_name=_("requirements"),
                        max_length=400,
                        blank=True,
                        help_text=_("List all the requirements that you expect from participants. (e.g. age restrictions, required skills etc) "
                                    "\nPlease insert each requirement per line.")
                    )
    region          = models.ForeignKey(
                        Region,
                        verbose_name=_("region"),
                        related_name=_("activities"),
                        related_query_name=_("activity"),
                        help_text=_("Choose a region where you activity will be held."),
                        on_delete=models.CASCADE
                    )
    tags            = models.ManyToManyField(
                        Tag,
                        verbose_name=_("tags"),
                        blank=True,
                        help_text=_("Select tag(s) that best describe your activity.")
                    )
    address         = models.CharField(
                        verbose_name=_("address"),
                        max_length=255,
                        help_text=_("Enter the address of the meeting place")
                    )
    latitude        = models.DecimalField(
                        verbose_name=_("latitude"),
                        max_digits=8,
                        decimal_places=5,
                        blank=True, null=True,
                    )
    longitude       = models.DecimalField(
                        verbose_name=_("longitude"),
                        max_digits=8,
                        decimal_places=5,
                        blank=True, null=True
                    )
    price           = models.DecimalField(
                        verbose_name=_("price"),
                        max_digits=6,
                        decimal_places=2,
                        default=0.00,
                        blank=True,
                        validators=[MinValueValidator(0.00)],
                        help_text=_("Cost of participation."
                                    "\nIf it's free, then leave it as 0.00 or blank")
                    )

    review_count    = models.IntegerField(blank=True, default=0, verbose_name=_("review count"))

    created         = models.DateTimeField(auto_now_add=True, verbose_name=_("activity created date"))
    modified        = models.DateTimeField(auto_now=True)
    approved        = models.BooleanField(verbose_name=_("is approved"), default=False)

    objects = ActivityManager()

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.title

    # Slugify the title as slug
    def save(self, *args, **kwargs):
        self.slug = init_slug = slugify(self.title)

        for x in itertools.count(1):
            if not Activity.objects.filter(slug=self.slug).exists():
                break
            self.slug = '{}-{}'.format(init_slug, x)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('activities:detail', kwargs={'slug': self.slug})

    # Returns the Requirements Value as a List by splitting the commas
    def requirements_as_list(self):
        return self.requirements.split('\n')

    # Returns the Highlights Value as a List by splitting the commas
    def highlights_as_list(self):
        return self.highlights.split('\n')

    # Checks if the activity is free or not
    def is_free(self):
        return self.price == 0.00 or self.price is None


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, related_name='images', on_delete=models.CASCADE)
    caption = models.CharField(max_length=60)
    image = models.ImageField(upload_to='activity_images/', blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
