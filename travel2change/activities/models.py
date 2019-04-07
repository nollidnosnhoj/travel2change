from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from autoslug import AutoSlugField
from cms.models.pluginmodel import CMSPlugin
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from users.models import Host

def get_featured_image_filename(instance, filename):
    """ Path to store activity's featured photo """
    return 'uploads/{0}/featured/{1}'.format(instance.pk, filename)

def get_photo_image_filename(instance, filename):
    """ Path where activity's photos are stored """
    return 'uploads/{0}/photos/{1}'.format(instance.activity.pk, filename)


class ActivityQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status="approved")
    
    def unapproved(self):
        return self.filter(status="unapproved")


class Region(models.Model):
    name = models.CharField(max_length=60, blank=False)
    slug = AutoSlugField(populate_from='name')

    objects = models.Manager()
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    font_awesome = models.CharField(max_length=60, blank=True, verbose_name=_('tag icon'),
        help_text=_('This will display an icon next to a tag. Format: fa-(icon name)'))

    objects = models.Manager()

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True, verbose_name=_('activity category'))
    font_awesome = models.CharField(max_length=60, blank=True, verbose_name=_('category icon'),
        help_text=_('This will display an icon next to a tag. Format: fa-(icon name)'))

    objects = models.Manager()

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Activity(models.Model):
    STATUS          = Choices('unapproved', 'approved')
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
    slug            = AutoSlugField(
                        populate_from='title',
                        always_update=True,
                    )
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
    categories      = models.ManyToManyField(
                        Category,
                        verbose_name=_('categories'),
                        blank=False,
                        help_text=_("Select categories the best fits your activity.")
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
                        help_text=_("Cost of participation."
                                    "\nIf it's free, then leave it as 0.00 or blank")
                    )
    featured_photo  = models.ImageField(
                        upload_to=get_featured_image_filename,
                        verbose_name=_('featured photo'),
                        null=True,
                        blank=True,
                        help_text=_('This photo will be featured on listings and the top'
                                    'of your activity page.')
                    )

    # Non Editable Fields (at least for users)
    status          = StatusField(default=STATUS.unapproved)
    approved_time   = MonitorField(monitor='status', when=['approved'])
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)
    is_featured     = models.BooleanField(verbose_name=_("is featured"), default=False)
    review_count    = models.IntegerField(blank=True, default=0, verbose_name=_("review count"))

    # Model Managers
    objects         = ActivityQuerySet.as_manager()

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activities:detail', kwargs={
            'region': self.region.slug,
            'slug': self.slug,
            'pk': self.pk
        })

    def requirements_as_list(self):
        # Returns the Requirements Value as a List by splitting the commas
        return self.requirements.split('\n')

    def highlights_as_list(self):
        # Returns the Highlights Value as a List by splitting the commas
        return self.highlights.split('\n')

    def get_bookmark_count(self):
        self.bookmark_set.all().count()

    @property
    def is_free(self):
        # Checks if the activity is free or not
        return self.price == 0.00 or self.price is None


class ActivityPhoto(models.Model):
    activity = models.ForeignKey(Activity, related_name='photos', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=get_photo_image_filename, verbose_name=_('Photo'))


"""                         ACTIVITY CMS PLUGINS                            """

class LatestActivities(CMSPlugin):
    latest_activities = models.IntegerField(
        default=5,
        help_text=_('The maximum number of latest activities to display')
    )

    def get_activities(self, request):
        queryset = Activity.objects.approved().order_by('-approved_time')
        return queryset[:self.latest_activities]

    def __str__(self):
        return ugettext('Latest activities: {0}'.format(self.latest_activities))


class FeaturedActivities(CMSPlugin):
    number_of_activities = models.IntegerField(
        default=5,
        help_text=_('The maximum number of featured activities to display')
    )

    def get_activities(self, request):
        queryset = Activity.objects.approved().filter(is_featured=True).order_by('-approved_time')
        return queryset[:self.number_of_activities]
    
    def __str__(self):
        return ugettext('Featured activities: {0}'.format(self.latest_activities))