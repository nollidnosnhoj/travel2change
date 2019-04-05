from django.conf import settings

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, reverse
from django.template.loader import render_to_string
from django.views.generic import DeleteView, ListView, UpdateView

from activities.models import Activity
from .forms import ApproveForm
from .mixins import StaffUserOnlyMixin

class ModerationActivityQueue(StaffUserOnlyMixin, ListView):
    model = Activity
    template_name = "moderations/moderation_queue.html"
    context_object_name = "activities"
    paginate_by = 10
    ordering = ['created']

    def get_queryset(self):
        # Order Unapproved Activities by Created Time Ascending
        return self.model.objects.unapproved().all()


class ActivityApprovalView(StaffUserOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    form_class = ApproveForm
    template_name = 'moderations/moderation_approval.html'
    success_message = 'Activity has successfully been approved! Email sent.'

    def form_valid(self, form):
        # Change status to approve, and send email to host
        instance = form.save(commit=False)
        instance.status = Activity.STATUS.approved
        send_notification(
            instance,
            "Your activity was approved!",
            "approval",
        )
        return super().form_valid(form)
    
    def send_mail(self, instance):
        msg = render_to_string('moderations/templates/approval.txt', {
            'activity': instance,
        })

        send_mail(
            'Your activity has been approved!',
            msg,
            settings.SERVER_EMAIL,
            [instance.host.user.email],
        )


class ActivityDisapprovalView(StaffUserOnlyMixin, DeleteView):
    success_message = "Activity has been successfully disapproved. Email sent."
    template_name = "moderations/moderation_disapproval.html"

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        # Notify users about disapproval, then delete object
        reasons = request.POST.get('reasons', 'N/A')
        send_notification(
            self.get_object(),
            "Your activity was disapproved.",
            "disapproval",
            reasons=reasons,
        )
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('moderations:queue')

def send_notification(instance, subject, template_prefix, **kwargs):
    # Send email notification to the host about approval/disapproval.
    template = "moderations/templates/{0}_email.txt".format(template_prefix)

    msg = render_to_string(template, {
        'activity': instance,
        **kwargs
    })

    send_mail(
        subject,
        msg,
        settings.SERVER_EMAIL,
        [instance.host.user.email],
    )
