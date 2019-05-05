from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.sites.models import Site

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
    'moderate_activity',
)


class Command(BaseCommand):
    help = 'Update to travel2change and create mod group'

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
        
        self.stdout.write(self.style.SUCCESS('Finished.'))
