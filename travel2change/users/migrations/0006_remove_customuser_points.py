# Generated by Django 2.1.7 on 2019-04-29 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_host_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='points',
        ),
    ]