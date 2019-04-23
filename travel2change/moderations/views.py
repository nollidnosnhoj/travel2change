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

class ModerationActivityQueue(StaffUserOnlyMixin, ListView):
    model = Activity
    template_name = "moderations/moderation_queue.html"
    context_object_name = "activities"
    paginate_by = 10

    def get_queryset(self):
        # Order Unapproved Activities by Created Time Ascending
        return self.model.objects.unapproved().all().order_by('created')


class ActivityApprovalView(StaffUserOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    fields = ('fh_item_id', )
    template_name = 'moderations/moderation_approval.html'
    success_message = 'Activity has successfully been approved! Email sent.'

    def form_valid(self, form):
        # Change status to approve, and send email to host
        instance = form.save(commit=False)
        instance.status = Activity.STATUS.approved
        send_notification(instance, "Your Activity Was Approved.", "approval")
        instance.save()
        return redirect(
            'activities:detail',
            region=instance.region.slug,
            slug=instance.slug,
        )
        return super().form_valid(form)


class ActivityDisapprovalView(StaffUserOnlyMixin, DeleteView):
    success_message = "Activity has been successfully disapproved. Email sent."
    template_name = "moderations/moderation_disapproval.html"
    success_url = reverse_lazy("moderations:queue")

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        # Notify users about disapproval, then delete object
        reasons = request.POST.get('reasons', 'N/A')
        activity = self.get_object()
        subject = "Your Activity Was Not Approved."
        send_notification(activity, subject, "disapproval", reasons=reasons)
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


def send_notification(instance, subject, template_prefix, **kwargs):
    # Send email notification to the host about approval/disapproval.
    template = "moderations/templates/{0}_email.txt".format(template_prefix)
    msg = render_to_string(template, {'activity': instance, **kwargs})
    send_mail(subject, msg, settings.SERVER_EMAIL, [instance.host.user.email], )
