# Generated by Django 2.1.7 on 2019-04-26 04:24

import activities.models
import activities.validators
import django.core.validators
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20190418_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredactivities',
            name='featured_tier',
            field=models.PositiveIntegerField(default=3, help_text='Activity with tiers higher than this number will be featured in the widget.', validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Featured Tier'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='featured_photo',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='This photo will be featured on listings and the topof your activity page.', null=True, upload_to=activities.models.get_featured_image_filename, validators=[activities.validators.validate_image_size], verbose_name='featured photo'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='is_featured',
            field=models.PositiveIntegerField(default=0, help_text='Each featured tier will determine if the activity will be featured in certain areas on the website.', validators=[django.core.validators.MaxValueValidator(5)], verbose_name='featured tier'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='review_count',
            field=models.IntegerField(default=0, verbose_name='review count'),
        ),
        migrations.AlterField(
            model_name='activityphoto',
            name='file',
            field=models.ImageField(upload_to=activities.models.get_photo_image_filename, validators=[activities.validators.validate_image_size], verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='featuredactivities',
            name='number_of_activities',
            field=models.IntegerField(default=5, help_text='The maximum number of featured activities to display.'),
        ),
        migrations.AlterField(
            model_name='featuredactivities',
            name='per_row',
            field=models.IntegerField(default=3, help_text='Number of activities per row.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Items per Row'),
        ),
        migrations.AlterField(
            model_name='latestactivities',
            name='latest_activities',
            field=models.IntegerField(default=5, help_text='The maximum number of latest activities to display. Insert "0" to show all'),
        ),
        migrations.AlterField(
            model_name='latestactivities',
            name='per_row',
            field=models.IntegerField(default=3, help_text='Number of activities per row.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Items per Row'),
        ),
        migrations.AlterField(
            model_name='region',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Image to display in region widget.', upload_to=activities.models.get_region_image_filename, validators=[activities.validators.validate_image_size]),
        ),
    ]
