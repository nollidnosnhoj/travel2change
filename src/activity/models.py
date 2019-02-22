from django.db import models

# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=400)
    hightlights = models.TextField(max_length=400)
    requirements = models.TextField(max_length=400, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    # Location Field

    def __str__(self):
        return self.title

class Region(models.Model):
    name = models.CharField(max_length=60, blank=False)
    image = models.ImageField(upload_to='region', height_field=100, width_field=100)
    
    def __str__(self):
        return self.name

class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, related_name='images')
    caption = models.CharField(max_length=60)
    image = models.ImageField(upload_to='activity_images/', blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    activities = models.ManyToManyField(Activity)
    font_awesome = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.name
