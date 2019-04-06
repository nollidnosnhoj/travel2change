from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Activity
from users.models import Host

""" Permission Mixin when Activity is set to Unapproved """
class CanViewUnapproved(object):
    def dispatch(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, kwargs['pk'])
        if activity.status == Activity.STATUS.unapproved:
            if request.user != activity.host.user or \
                not request.user.is_staff or \
                    not request.user.is_superuser:
                raise Http404
        return super().dispatch(request, *args, **kwargs)


""" Users that owns an activity can only view the object """
class OwnershipViewOnly(object):
    def dispatch(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, kwargs['pk'])
        if request.user != activity.host.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


""" Host can only view """
class HostOnlyView(object):
    def dispatch(self, request, *args, **kwargs):
        host = Host.objects.filter(user=request.user)
        if not host:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
