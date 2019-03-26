from django.utils.translation import ugettext as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class ActivitiesApp(CMSApp):
    app_name = "activities"
    name = _("Activity Apphook")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["activities.urls"]
