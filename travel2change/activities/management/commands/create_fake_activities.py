import lorem
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Max
from activities.models import Region, Tag, Category, Activity
from users.models import Host

User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates number of activities created.')
    
    def handle(self, *args, **options):
        # Get super user
        try:
            vip = User.objects.get(pk=1)
        except User.DoesNotExist:
            raise Exception('Please create a superuser')
        
        # Get (or Create) User's Host Profile
        host, created = Host.objects.get_or_create(user=vip)

        # Check if there are regions, categories, or tags
        region_exists = Region.objects.first()
        cat_exists = Category.objects.first()
        tag_exists = Tag.objects.first()

        if region_exists and cat_exists and tag_exists:
            # Get the max pk for regions, categories, and tags
            max_region_pk = Region.objects.all().aggregate(max_pk=Max('pk')).get('max_pk')
            max_cat_pk = Category.objects.all().aggregate(max_pk=Max('pk')).get('max_pk')
            max_tag_pk = Tag.objects.all().aggregate(max_pk=Max('pk')).get('max_pk')

            # Get total arg
            total = options['total']

            # If total param passed and it's greater than zero
            if total and total > 0:
                for i in range(total):
                    # Parse highlights and requirements
                    highlights = lorem.paragraph().replace('. ', '\n')[:400]
                    requirements = lorem.paragraph().replace('. ', '\n')
                    # Get random region and cat pk
                    region_pk = random.randint(1, max_region_pk)
                    cat_pk = random.randint(1, max_cat_pk)
                    # Get random number of tags to have
                    num_tag = random.randint(0, max_tag_pk)
                    # create activity instance
                    instance = Activity.objects.create(
                        host=host,
                        title=lorem.sentence()[:255],
                        description=lorem.paragraph()[:400],
                        highlights=highlights,
                        requirements=requirements,
                        region=Region.objects.get(pk=region_pk),
                        address='Somewhere',
                        is_featured=random.randint(0, 5),
                    )
                    is_approved = random.randint(0, 5)
                    instance.status = 'approved' if is_approved > 0 else 'unapproved'
                    cat = Category.objects.get(pk=cat_pk)
                    # Get random number of tags to set
                    tag_list = set()
                    for i in range(num_tag):
                        tag_pk = random.randint(1, max_tag_pk)
                        tag_list.add(Tag.objects.get(pk=tag_pk))
                    instance.categories.add(cat)
                    instance.tags.set(list(tag_list))
                    instance.save()
                    self.stdout.write(self.style.SUCCESS('Activity saved.'))
        else:
            raise Exception("There must be at least one region, category, and tag object.")
        
        self.stdout.write("Script completed.")
