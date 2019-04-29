from django import template
from activities.models import Activity

register = template.Library()

@register.simple_tag
def new_activities():
    return Activity.objects.unapproved().count()
