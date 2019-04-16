from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponseRedirect
)

class StaffUserOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
