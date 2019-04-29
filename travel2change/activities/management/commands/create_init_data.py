from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.sites.models import Site
from django.utils.text import slugify
from activities.models import Region, Tag, Category

User = get_user_model()

mod_group_perms = (
    'view_activity',
    'add_activity',
    'change_activity',
    'delete_activity',
    'view_host',
    'change_host',
    'view_activityphoto',
    'add_activityphoto',
    'change_activityphoto',
    'delete_activityphoto',
)

regions_name = (
    'Island Of Hawaii',
    'Kauai',
    'Maui',
    'Oahu East',
    'Oahu North',
    'Oahu South',
    'Oahu West',
)

regions_slug = tuple(map(slugify, regions_name))

categories_name = (
    'Culture Perservation',
    'Environmental Impact',
    'Nature',
    'Social Impact',
    'Water Activities',
)

categories_slug = tuple(map(slugify, categories_name))

tags_name = (
    'Donation Suggested',
    'Easy',
    'Family Friendly',
    'Food Included',
    'Intermediate',
    'Intense',
)

tags_slug = tuple(map(slugify, tags_name))


class Command(BaseCommand):
    help = 'Create the default regions, categories, and tags'

    def handle(self, *args, **options):
        
        # Modify site information
        site = Site.objects.get(pk=1)
        site.name = 'travel2change'
        site.domain = settings.SITE_DOMAIN
        site.save()
        self.stdout.write('Site Information Updated.')

        # create moderation group
        mod_group, created = Group.objects.get_or_create(name="Moderators")
        if created:
            for i in mod_group_perms:
                mod_group.permissions.add(Permission.objects.get(codename=i))
                self.stdout.write('{0} permission is added.'.format(i))
            self.stdout.write(self.style.SUCCESS('{0} group created!'.format(mod_group.name)))
        else:
            self.stdout.write('{0} already created'.format(mod_group.name))

        # Generate regions, categories, and tags
        for i in range(len(regions_name)):
            region, created = Region.objects.get_or_create(name=regions_name[i], slug=regions_slug[i])
            if created:
                region.save()
                self.stdout.write(self.style.SUCCESS('{0} created!'.format(regions_name[i])))
            else:
                self.stdout.write('{0} already created'.format(regions_name[i]))

        for i in range(len(categories_name)):
            cat, created = Category.objects.get_or_create(name=categories_name[i], slug=categories_slug[i])
            if created:
                cat.save()
                self.stdout.write(self.style.SUCCESS('{0} created!'.format(categories_name[i])))
            else:
                self.stdout.write('{0} already created'.format(categories_name[i]))

        for i in range(len(tags_name)):
            tag, created = Tag.objects.get_or_create(name=tags_name[i], slug=tags_slug[i])
            if created:
                tag.save()
                self.stdout.write(self.style.SUCCESS('{0} created!'.format(tags_name[i])))
            else:
                self.stdout.write('{0} already created'.format(tags_name[i]))
        
        self.stdout.write(self.style.SUCCESS('Successfully created regions, categories, and tags'))
