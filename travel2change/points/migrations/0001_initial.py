# Generated by Django 2.1.7 on 2019-04-23 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardedPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=255, verbose_name='reason')),
                ('points', models.IntegerField(default=0, verbose_name='points')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PointValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Choose a key name of this point value', max_length=50, verbose_name='key')),
                ('value', models.IntegerField(default=0, verbose_name='value')),
            ],
        ),
        migrations.AddField(
            model_name='awardedpoint',
            name='point_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='points.PointValue'),
        ),
        migrations.AddField(
            model_name='awardedpoint',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awardedpoint_target', to=settings.AUTH_USER_MODEL),
        ),
    ]
