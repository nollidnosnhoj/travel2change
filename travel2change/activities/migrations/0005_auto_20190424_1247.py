# Generated by Django 2.1.7 on 2019-04-24 22:47

import activities.models
import activities.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20190423_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='featured_photo',
            field=models.ImageField(default='defaults/default_activity.jpg', help_text='This photo will be featured on listings and the topof your activity page.', upload_to=activities.models.get_featured_image_filename, validators=[activities.validators.validate_image_size], verbose_name='featured photo'),
        ),
        migrations.AlterField(
            model_name='activityphoto',
            name='file',
            field=models.ImageField(upload_to=activities.models.get_photo_image_filename, validators=[activities.validators.validate_image_size], verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='region',
            name='image',
            field=models.ImageField(blank=True, help_text='Image to display in region widget.', upload_to=activities.models.get_region_image_filename, validators=[activities.validators.validate_image_size]),
        ),
    ]
