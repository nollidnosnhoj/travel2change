from django.contrib.auth.mixins import AccessMixin
from django.http import Http404

class UnapprovedActivityMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.object.is_approved:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            if self.object.host.user != request.user:
                if not request.user.is_staff and not request.user.is_superuser:
                    raise Http404("Activity has not been approved yet.")
        return super().dispatch(request, *args, **kwargs)


class ReviewCheck(object):
    def has_review_permission(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return False
        if not self.object.is_approved:
            return False
        if self.object.host.user == request.user:
            return False
        return self.object.reviews.count() < 1
