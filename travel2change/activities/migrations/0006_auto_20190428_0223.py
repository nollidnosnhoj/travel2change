# Generated by Django 2.1.7 on 2019-04-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20190427_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(help_text='Briefly describe your activity.', max_length=400, verbose_name='description'),
        ),
    ]
