from django.contrib.sitemaps import Sitemap
from .models import Activity

class ActivitySitemap(Sitemap):
    changefreq = "daily"
    def items(self):
        return Activity.objects.approved().all()
