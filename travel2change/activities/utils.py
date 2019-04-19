from reviews.models import Review
from .models import Activity

def check_if_user_can_review(request, activity):
    """ Checks if the request.user is eligible to review based on business logic """
    if not hasattr(request, 'user'):
        return False
    if not isinstance(activity, Activity):
        return False
    if not request.user.is_authenticated:
        return False
    if activity.status == Activity.STATUS.unapproved:
        return False
    if activity.host.user == request.user:
        return False
    return Review.objects.filter(activity=activity).count() < 1
