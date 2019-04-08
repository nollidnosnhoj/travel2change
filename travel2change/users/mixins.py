from django.core.exceptions import PermissionDenied
from users.models import Host

class UserIsHostViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        host = Host.objects.filter(user=request.user)
        if not host:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
