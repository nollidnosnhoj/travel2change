from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from activities.models import Activity

class UnapprovedActivityMixin(AccessMixin):
    """ This sets permissions for unapproved activities """

    def dispatch(self, request, *args, **kwargs):
        if not isinstance(self.object, Activity):
            raise ImproperlyConfigured("object must be an instance of Activity")
        # if the activity has not been approved yet
        if not self.object.is_approved:
            # If anonymous user
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            # If the user is not the host of the activity
            if self.object.host.user != request.user:
                # If the user does not have moderation permission
                if not request.user.has_perm('activities.moderate_activity'):
                    raise Http404("Activity is either awaiting approval, or inactive.")
        return super().dispatch(request, *args, **kwargs)
