from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext as _

@apphook_pool.register
class ActivityApp(CMSApp):
    app_name = _("activity")
    name = _("Activity Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["activity.urls"]
