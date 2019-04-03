from django.views.generic import ListView

from activities.models import Activity
from .mixins import StaffUserOnlyMixin

class ModerationActivityQueue(StaffUserOnlyMixin, ListView):
    model = Activity
    paginate_by = 10

    def get_queryset(self):
        # Order Unapproved Activities by Created Time Ascending
        return self.model.objects.unapproved().order_by('+created')
