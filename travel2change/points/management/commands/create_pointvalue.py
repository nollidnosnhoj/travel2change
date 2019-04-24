from django.core.management.base import BaseCommand
from points.models import PointValue

class Command(BaseCommand):
    help = 'Create PointValue objects to avoid Exceptions'

    def handle(self, *args, **options):
        pv1 = PointValue(key='review_create', value=20)
        pv1.save()
        pv2 = PointValue(key='review_photo', value=10)
        pv2.save()

        self.stdout.write(self.style.SUCCESS('Default pointvalue created.'))
