from django.conf import settings
from django.http import Http404
from django.http import (
    HttpResponseRedirect
)

class StaffUserOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)
        if not request.user.is_staff and not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
