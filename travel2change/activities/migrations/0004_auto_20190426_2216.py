# Generated by Django 2.1.7 on 2019-04-27 08:16

import activities.models
import activities.validators
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20190425_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='font_awesome',
        ),
        migrations.AlterField(
            model_name='activity',
            name='featured_photo',
            field=sorl.thumbnail.fields.ImageField(help_text='This photo will be featured on listings and the topof your activity page.', upload_to=activities.models.get_featured_image_filename, validators=[activities.validators.validate_image_size], verbose_name='featured photo'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='font_awesome',
            field=models.CharField(blank=True, help_text='This will display an icon next to a tag. Format: <i class="(icon name)"></i>', max_length=60, verbose_name='tag icon'),
        ),
    ]
