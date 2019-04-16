from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Activity

class CanViewUnapprovedMixin(object):
    """ If activity is not approved, users that aren't staff
        or owner of the activity will be blocked """
    def dispatch(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=kwargs['pk'])
        if activity.status == Activity.STATUS.unapproved:
            if request.user != activity.host.user and (not request.user.is_staff and not request.user.is_superuser):
                raise Http404
        return super().dispatch(request, *args, **kwargs)
