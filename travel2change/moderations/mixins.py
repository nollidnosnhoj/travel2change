from django.contrib.auth.mixins import PermissionRequiredMixin


class ModeratorsOnlyMixin(PermissionRequiredMixin):
    # Only users with the required permissions can view
    permission_required = (
        'activities.view_activity',
        'activities.add_activity',
        'activities.change_activity',
        'activities.delete_activity',
    )
