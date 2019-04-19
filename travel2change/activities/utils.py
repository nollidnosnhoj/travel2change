from reviews.models import Review
from .models import Activity

def check_if_user_can_review(activity, request):
    if not isinstance(activity, Activity):
        return False
    if not request.user.is_authenticated:
        return False
    if activity.status == Activity.STATUS.unapproved:
        return False
    if activity.host.user == request.user:
        return False
    return Review.objects.filter(activity=activity).count() < 1


def construct_fareharbor_widget(activity):
    if not isinstance(activity, Activity):
        return False
    fh_string = '<script src="https://fareharbor.com/embeds/script/calendar/%s/items/%s/?fallback=simple&flow=18919"></script>'
    if activity.is_free:
        if activity.fh_item_id:
            return fh_string % ('travel2change', activity.fh_item_id)
        else:
            return "FareHarbor Item ID was not provided."
    else:
        if activity.fh_item_id and activity.host.fh_username:
            return fh_string % (activity.host.fh_username, activity.fh_item_id)
        else:
            if not activity.host.fh_username:
                return "Activity host must have a FareHarbor username"
    return "FareHarbor Item ID was not provided."
