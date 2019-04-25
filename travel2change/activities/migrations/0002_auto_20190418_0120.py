# Generated by Django 2.1.7 on 2019-04-18 11:20

import activities.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionsPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='activities_regionspluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('per_row', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Items per Row')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='featuredactivities',
            name='per_row',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Items per Row'),
        ),
        migrations.AddField(
            model_name='latestactivities',
            name='per_row',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Number of Items per Row'),
        ),
        migrations.AddField(
            model_name='region',
            name='image',
            field=models.ImageField(blank=True, help_text='Image to display in region widget.', upload_to=activities.models.get_region_image_filename),
        ),
        migrations.AddField(
            model_name='regionspluginmodel',
            name='regions',
            field=models.ManyToManyField(to='activities.Region'),
        ),
    ]