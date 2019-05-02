from django.conf import settings
from django.core.mail.message import EmailMessage
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from activities.models import Activity
from .mixins import ModeratorsOnlyMixin

# Shows all the unapproved (awaiting approval) activities in a view
# Only staff users (is_staff or is_superuser) can access it
class ModerationActivityQueue(ModeratorsOnlyMixin, ListView):
    model = Activity
    template_name = "moderations/moderation_queue.html"
    context_object_name = "activities"

    def get_queryset(self):
        return self.model.objects.unapproved().all().order_by('created')


# A Confirmation View for Approving Activity
class ActivityApprovalView(ModeratorsOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    fields = ('fh_item_id', )
    template_name = 'moderations/moderation_approval.html'
    success_message = 'Activity has successfully been approved! Email sent.'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # FareHarbor item is required to proceed.
        if self.object.fh_item_id is None:
            messages.error(self.request, "Please enter a FareHarbor Item ID for this activity before approving.")
            return redirect(self.object)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.status = Activity.STATUS.approved
        # send approval email
        send_notification(
            self.request,
            instance,
            "Your Activity Was Approved.",
            "approval",
            url=self.request.build_absolute_uri(instance.get_absolute_url()),
        )
        instance.save()
        return super().form_valid(form)


class ActivityDisapprovalView(ModeratorsOnlyMixin, DeleteView):
    success_message = "Activity has been successfully disapproved. Email sent."
    template_name = "moderations/moderation_disapproval.html"
    success_url = reverse_lazy("moderations:queue")

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        reasons = request.POST.get('reasons', 'N/A')
        activity = self.get_object()
        subject = "Your Activity Was Not Approved."
        # send disapproval email
        send_notification(
            request,
            activity,
            subject,
            "disapproval",
            reasons=reasons
        )
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


def send_notification(request, instance, subject, template_prefix, **kwargs):
    """
    Send email to the activity's host.

    template can be found in => templates/moderations/templates/
    
    Paramters:
        instance - the activity instance.
        subject - The subject line
        template_prefix - Template prefix that the email will use.

    https://docs.djangoproject.com/en/2.2/topics/email/
    """
    template = "moderations/templates/{0}_email.txt".format(template_prefix)
    context = {
        'activity': instance,
        **kwargs
    }
    msg = render_to_string(template_name=template, context=context)
    notif_mail = EmailMessage(
        subject=subject,
        body=msg,
        from_email=settings.SERVER_EMAIL,
        to=[instance.host.user.email],
    )
    notif_mail.send()
