from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from activities.models import LatestActivities, FeaturedActivities

@plugin_pool.register_plugin
class LatestActivitiesPlugin(CMSPluginBase):
    model = LatestActivities
    name = _("Latest Activities")
    render_template = 'activities/plugins/latest.html'
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['activities'] = instance.get_activities(request)
        return context


@plugin_pool.register_plugin
class FeaturedActivitiesPlugin(CMSPluginBase):
    model = FeaturedActivities
    name = _('Featured Activities')
    render_template = 'activities/plugins/latest.html'
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['activities'] = instance.get_activities(request)
        return context
