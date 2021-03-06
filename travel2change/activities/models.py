import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext, ugettext_lazy as _
from autoslug import AutoSlugField
from cms.models.pluginmodel import CMSPlugin
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from sorl.thumbnail import ImageField
from users.models import Host
from .validators import validate_image_size


User = get_user_model()

def get_featured_image_filename(instance, filename):
    """ Path for activity's featured photos """
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'uploads/activities/featured-photos/activity_{0}.{1}'.format(instance.pk, ext)
    else:
        return 'uploads/activities/featured-photos/{0}.{1}'.format(uuid.uuid4().hex, ext)

def get_photo_image_filename(instance, filename):
    """ Path where activity's photos are stored """
    ext = filename.split('.')[-1]
    return 'uploads/activities/photos/{0}.{1}'.format(uuid.uuid4().hex, ext)

def get_region_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'uploads/regions/region_{0}.{1}'.format(instance.pk, ext)
    else:
        return 'uploads/regions/{0}.{1}'.format(uuid.uuid4().hex, ext)


class ActivityQuerySet(models.QuerySet):
    """ Activity Queries """

    def approved(self):
        """ Query approved activities """
        return self.filter(status="approved")
    
    def unapproved(self):
        """ Query unapproved activities """
        return self.filter(status="unapproved")
    
    def inactive(self):
        return self.filter(status='inactive')

    def free(self):
        """ Query free activities """
        return self.approved().filter(is_free=True)
    
    def paid(self):
        """ Query paid activities """
        return self.approved().filter(is_free=False)

    def featured(self):
        """ Query featured activities (Greater than tier 0)"""
        return self.approved().filter(is_featured__gt=0)

class Region(models.Model):
    """
    Create a Region instance.
    Parameters:
        name (CharField) - Name of the region
        slug (SlugField) - Name of the region in slug form. (alphanumeric, hyphens, and underscores)
        image (ImageField) - Image to display in region widget.
    """
    name = models.CharField(max_length=60, blank=False, help_text=_('Name of the region'))
    slug = models.SlugField(max_length=20, unique=True,
        help_text=_('Name of the region in slug form. (alphanumeric, hyphens, and underscores)'))
    image = ImageField(
        upload_to=get_region_image_filename,
        blank=True,
        help_text=_('Image to display in region widget.'),
        validators=[validate_image_size],
    )
    objects = models.Manager()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def get_image_url(self):
        """ Get region's image if available. If not, show placeholder """
        if self.image:
            return self.image.url
        else:
            return '/media/defaults/default_region.jpg'
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Create a Tag instance.
    Paramters:
        name (CharField) - Name of the tag
        slug (SlugField) - Name of the tag in slug form (alphanumeric, hyphen, and underscores)
        font_awesome (CharField) - This will display an icon next to a tag. Format: <i class="(icon name)"></i>
    """
    name = models.CharField(max_length=60, blank=False, null=False, unique=True,
        help_text=_('Name of the tag'))
    slug = models.SlugField(max_length=20, unique=True,
        help_text=_('Name of the tag in slug form (alphanumeric, hyphen, and underscores)'))
    font_awesome = models.CharField(max_length=60, blank=True, verbose_name=_('tag icon'),
        help_text=_('This will display an icon next to a tag. Format: <i class="(icon name)"></i>'))

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class Category(models.Model):
    """
    Create a Category instance.
    Parameters:
        name (CharField) - Name of the region
        slug (SlugField) - Name of the region in slug form. (alphanumeric, hyphens, and underscores)
    """
    name = models.CharField(max_length=60, blank=False, null=False, unique=True,
        help_text=_('Name of the category'))
    slug = models.SlugField(max_length=20, unique=True,
        help_text=_('Name of the category in slug form (alphanumeric, hyphens, and underscores)'))

    objects = models.Manager()

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Activity(models.Model):
    """
    Create an Activity instance
    Parameters:
        host (ForeignKey, Host)
        title (CharField) - title of the activity
        slug (AutoSlugField) - Auto generate a slug based on the title of the activity
        description (CharField) - Briefly describe your activity
        highlights (CharField) - List what makes this activity unique. New line = new bullet
        requirements (CharField) - List what the participants require to participate. New line = new bullet
        region (ForeignKey, Region) - Choose a region where your activity takes place
        categories (ManyToManyField, Category) - Select what type(s) of activity you are hosting
        tags (ManyToManyField, Tag) - Select tag(s) that best describe your activity
        address (CharField) - Enter a meeting place for the activity
        latitude (DecimalField) - max_digits=9, decimal_places=6
        longitude (DecimalField) - max_digits=9, decimal_places=6
        price (DecimalField) - price of activity. leave blank or 0 if free.
        featured_photo (ImageField) - This image will show up on your activity card when browsing
        fh_item_id (PositiveIntegerField) - FareHarbor item ID
        
        status (StatusField) - either approved or unapproved. default to unapproved.
    """
    STATUS          = Choices('unapproved', 'approved', 'inactive', )
    host            = models.ForeignKey(
                        Host,
                        related_name=_("host"),
                        on_delete=models.CASCADE,
                        help_text=_('The host that is hosting the activity.')
                    )
    title           = models.CharField(
                        verbose_name=_("title"),
                        max_length=255,
                        blank=False,
                        null=False,
                        help_text=_("Give a name for your activity that will attract travelers."),
                    )
    slug            = AutoSlugField(
                        populate_from='title',
                        always_update=True,
                    )
    description     = models.TextField(
                        verbose_name=_("description"),
                        max_length=400,
                        help_text=_("Briefly describe your activity.")
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
                        help_text=_("Choose a region where your activity takes place."),
                        on_delete=models.CASCADE
                    )
    categories      = models.ManyToManyField(
                        Category,
                        verbose_name=_('categories'),
                        blank=False,
                        help_text=_("Select what type(s) of activity you are hosting.")
                    )
    tags            = models.ManyToManyField(
                        Tag,
                        verbose_name=_("tags"),
                        blank=True,
                        help_text=_("Select tag(s) that best describe your activity.")
                    )
    address         = models.CharField(
                        verbose_name=_("meeting place"),
                        max_length=255,
                        help_text=_("Enter a meeting place for the activity")
                    )
    latitude        = models.DecimalField(
                        verbose_name=_("latitude"),
                        max_digits=9,
                        decimal_places=6,
                        default=21.307,
                        blank=True, null=True,
                    )
    longitude       = models.DecimalField(
                        verbose_name=_("longitude"),
                        max_digits=9,
                        decimal_places=6,
                        default=-157.858,
                        blank=True, null=True
                    )
    price           = models.DecimalField(
                        verbose_name=_("price"),
                        max_digits=6,
                        decimal_places=2,
                        default=0.00,
                        blank=True,
                        validators=[MinValueValidator(0.00)],
                        help_text=_("Cost for participating. Leave blank or 0 if it's free.")
                    )
    featured_photo  = ImageField(
                        upload_to=get_featured_image_filename,
                        verbose_name=_('featured photo'),
                        blank=False,
                        help_text=_('This image will show up on your activity card when browsing.'),
                        validators=[validate_image_size],
                    )
    fh_item_id      = models.PositiveIntegerField(
                        verbose_name=_('fareharbor item id'),
                        blank=True,
                        null=True,
                        default=None,
                        help_text=_('This is the ID number of your FareHarbor item. Leave blank if your activity is free.')
                    )

    """ Private fields """

    # Activity status (Approved or Unapproved)
    status          = StatusField(default=STATUS.unapproved, help_text=_('What is the current status of the activity?'))
    # Time when activity status is approved
    created   = MonitorField(monitor='status', when=['approved'])
    # Time when activity is modified
    modified        = models.DateTimeField(auto_now=True)
    # Boolean field to check if activity is featured
    is_featured     = models.PositiveIntegerField(
                        blank=False,
                        default=0,
                        verbose_name=_("featured tier"),
                        validators=[MaxValueValidator(5)],
                        help_text=_('Each featured tier will determine if the activity will be featured in certain areas on the website.')
                    )

    objects         = ActivityQuerySet.as_manager()

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
        permissions = (
            # This permission allows them to view unapproved activities and moderation queue.
            ('moderate_activity', 'Can Moderate Activity'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activities:detail', kwargs={
            'region': self.region.slug,
            'slug': self.slug,
        })

    def requirements_as_list(self):
        # Returns the Requirements Value as a List by splitting the commas
        return self.requirements.split('\n')

    def highlights_as_list(self):
        # Returns the Highlights Value as a List by splitting the commas
        return self.highlights.split('\n')
    
    @property
    def favorite_count(self):
        return self.favorite_set.all().count()

    @property
    def is_free(self):
        # Checks if the activity is free or not
        return self.price == 0.00 or self.price is None
    
    @property
    def is_approved(self):
        # Check if activity is approved
        return self.status == self.STATUS.approved

    @property
    def average_rating(self):
        # Accumulate average ratings based on activity's review
        avg_rating = self.reviews.all().aggregate(Avg('rating')).get('rating__avg')
        if avg_rating is None:
            return 0.00
        return avg_rating
    
    @property
    def review_count(self):
        # Count all the reviews for the activity
        return self.reviews.all().count()


class ActivityPhoto(models.Model):
    activity        = models.ForeignKey(Activity, related_name='photos', on_delete=models.CASCADE)
    file            = models.ImageField(upload_to=get_photo_image_filename, verbose_name=_('Photo'), validators=[validate_image_size], )


"""                         ACTIVITY CMS PLUGINS                            """


class LatestActivities(CMSPlugin):
    # CMS Plugin for Latest Activities
    per_row = models.IntegerField(
        verbose_name=_('Number of Items per Row'),
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text=_('Number of activities per row.')
    )
    latest_activities = models.IntegerField(
        default=5,
        help_text=_('The maximum number of latest activities to display. Insert "0" to show all')
    )

    def get_activities(self, request):
        queryset = Activity.approved.all()
        return queryset[:self.latest_activities]
    
    def get_per_rows(self, request):
        return self.per_row

    def __str__(self):
        return ugettext('Latest activities: {0}'.format(self.latest_activities))


class FeaturedActivities(CMSPlugin):
    # CMS Plugin for Featured Activities
    per_row = models.IntegerField(
        verbose_name=_('Number of Items per Row'),
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text=_('Number of activities per row.')
    )

    number_of_activities = models.IntegerField(
        default=5,
        help_text=_('The maximum number of featured activities to display.')
    )

    featured_tier = models.PositiveIntegerField(
        verbose_name=_('Featured Tier'),
        default=3,
        validators=[MaxValueValidator(5)],
        help_text=_('Activity with tiers higher than this number will be featured in the widget.')
    )

    def get_activities(self, request):
        queryset = Activity.objects.approved()
        queryset = queryset.filter(is_featured__gte=self.featured_tier)
        return queryset[:self.number_of_activities]
    
    def get_per_rows(self, request):
        return self.per_row
    
    def __str__(self):
        return ugettext('Featured activities: {0}'.format(self.number_of_activities))


class RegionsPluginModel(CMSPlugin):
    # CMS Plugin for Regions
    per_row = models.IntegerField(
        verbose_name=_('Number of Items per Row'),
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    regions = models.ManyToManyField(Region)

    def copy_relations(self, old_instance):
        self.regions.set(old_instance.regions.all())

    def get_regions(self, request):
        return self.regions.all()
    
    def get_per_rows(self, request):
        return self.per_row

    def __str__(self):
        return ugettext('Regions Widget')
