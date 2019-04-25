# Generated by Django 2.1.7 on 2019-04-25 12:00

import activities.models
import activities.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20190424_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='featured_photo',
            field=models.ImageField(default='defaults/default_featured_activity.jpg', help_text='This photo will be featured on listings and the topof your activity page.', upload_to=activities.models.get_featured_image_filename, validators=[activities.validators.validate_image_size], verbose_name='featured photo'),
        ),
    ]
