from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Activity
from users.models import Host

class CanViewUnapproved(object):
    """ If activity is not approved, users that aren't staff
        or owner of the activity will be blocked """
    def dispatch(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=kwargs['pk'])
        if activity.status == Activity.STATUS.unapproved:
            if request.user != activity.host.user or \
                not request.user.is_staff or \
                    not request.user.is_superuser:
                raise Http404
        return super().dispatch(request, *args, **kwargs)


class OwnershipViewOnly(object):
    """ Users that created the activity can view only """
    def dispatch(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=kwargs['pk'])
        if request.user != activity.host.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class HostOnlyView(object):
    """ Only hosts can view """
    def dispatch(self, request, *args, **kwargs):
        host = Host.objects.filter(user=request.user)
        if not host:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
