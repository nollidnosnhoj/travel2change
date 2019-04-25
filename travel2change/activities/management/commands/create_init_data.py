from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from activities.models import Region, Tag, Category

User = get_user_model()

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
    'Transportation Included',
    'Transportation Upon Request',
)

tags_slug = tuple(map(slugify, tags_name))


class Command(BaseCommand):
    help = 'Create the default regions, categories, and tags'

    def handle(self, *args, **options):
        for i in range(len(regions_name)):
            region, created = Region.objects.get_or_create(name=regions_name[i], slug=regions_slug[i])
            if created:
                region.save()
        for i in range(len(categories_name)):
            cat, created = Category.objects.get_or_create(name=categories_name[i], slug=categories_slug[i])
            if created:
                cat.save()
        for i in range(len(tags_name)):
            tag, created = Tag.objects.get_or_create(name=tags_name[i], slug=tags_slug[i])
            if created:
                tag.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully created regions, categories, and tags'))
