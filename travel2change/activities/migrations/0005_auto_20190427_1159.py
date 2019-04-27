# Generated by Django 2.1.7 on 2019-04-27 21:59

import activities.models
import activities.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20190426_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='categories',
            field=models.ManyToManyField(help_text='Select what type(s) of activity you are hosting.', to='activities.Category', verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(help_text='Briefly describe your activity.', max_length=400, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='featured_photo',
            field=sorl.thumbnail.fields.ImageField(help_text='This image will show up on your activity card when browsing.', upload_to=activities.models.get_featured_image_filename, validators=[activities.validators.validate_image_size], verbose_name='featured photo'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='fh_item_id',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='This is the ID number of your FareHarbor item. Leave blank if your activity is free.', null=True, verbose_name='fareharbor item id'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='host',
            field=models.ForeignKey(help_text='The host that is hosting the activity.', on_delete=django.db.models.deletion.CASCADE, related_name='host', to='users.Host'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text="Cost for participating. Leave blank or 0 if it's free.", max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='region',
            field=models.ForeignKey(help_text='Choose a region where your activity takes place.', on_delete=django.db.models.deletion.CASCADE, related_name='activities', related_query_name='activity', to='activities.Region', verbose_name='region'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(help_text='Give a name for your activity that will attract travelers.', max_length=255, verbose_name='title'),
        ),
    ]
