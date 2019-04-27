from django.conf import settings

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from activities.models import Activity
from .mixins import StaffUserOnlyMixin

# Shows all the unapproved (awaiting approval) activities in a view
# Only staff users (is_staff or is_superuser) can access it
class ModerationActivityQueue(StaffUserOnlyMixin, ListView):
    model = Activity
    template_name = "moderations/moderation_queue.html"
    context_object_name = "activities"

    def get_queryset(self):
        return self.model.objects.unapproved().all().order_by('created')


# A Confirmation View for Approving Activity
class ActivityApprovalView(StaffUserOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    fields = ('fh_item_id', )
    template_name = 'moderations/moderation_approval.html'
    success_message = 'Activity has successfully been approved! Email sent.'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.fh_item_id is None:
            messages.error(self.request, "Please enter a FareHarbor Item ID for this activity before approving.")
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.status = Activity.STATUS.approved
        send_notification(instance, "Your Activity Was Approved.", "approval")
        instance.save()
        return super().form_valid(form)


class ActivityDisapprovalView(StaffUserOnlyMixin, DeleteView):
    success_message = "Activity has been successfully disapproved. Email sent."
    template_name = "moderations/moderation_disapproval.html"
    success_url = reverse_lazy("moderations:queue")

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        reasons = request.POST.get('reasons', 'N/A')
        activity = self.get_object()
        subject = "Your Activity Was Not Approved."
        send_notification(activity, subject, "disapproval", reasons=reasons)
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


def send_notification(instance, subject, template_prefix, **kwargs):
    """
    Send email to the activity's host.

    template can be found in => templates/moderations/templates/
    
    Paramters:
        instance - the activity instance.
        subject - The subject line
        template_prefix - Template prefix that the email will use.
    """
    template = "moderations/templates/{0}_email.txt".format(template_prefix)
    msg = render_to_string(template, {'activity': instance, **kwargs})
    send_mail(subject, msg, settings.SERVER_EMAIL, [instance.host.user.email], )
