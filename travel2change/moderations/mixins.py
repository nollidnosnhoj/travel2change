from django.contrib.auth.mixins import PermissionRequiredMixin


class ModeratorsOnlyMixin(PermissionRequiredMixin):
    # Only users with the required permissions can view
    permission_required = ('activities.moderate_activity', )
