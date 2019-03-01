# Generated by Django 2.1.7 on 2019-03-01 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(help_text='Describe the activity. (Max. 400 characters)', max_length=400, verbose_name='description')),
                ('highlights', models.TextField(help_text='List what makes this activity unique. (Max. 400 characters)', max_length=400, verbose_name='highlights')),
                ('requirements', models.TextField(blank=True, help_text='List all the requirements that you expect from participants. (e.g. age restrictions, required skills etc)', max_length=400, verbose_name='requirements')),
                ('address', models.CharField(help_text='Enter the address of the meeting place', max_length=255, verbose_name='address')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='latitude')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='longitude')),
                ('price', models.DecimalField(decimal_places=2, help_text='Cost of participation. Enter "0.00" if the activity is free.', max_digits=6, verbose_name='price')),
                ('review_count', models.IntegerField(blank=True, default=0, verbose_name='review count')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='activity created date')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
            managers=[
                ('activities', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=60)),
                ('image', models.ImageField(upload_to='activity_images/')),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='activity.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('image', models.ImageField(upload_to='region')),
            ],
            managers=[
                ('regions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('font_awesome', models.CharField(max_length=60)),
            ],
            managers=[
                ('tags', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Region', verbose_name='region'),
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='activity.Tag', verbose_name='tags'),
        ),
    ]
