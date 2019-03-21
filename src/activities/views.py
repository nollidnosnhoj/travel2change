from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from formtools.wizard.views import SessionWizardView
from .forms import ActivityUpdateForm, PhotoUploadForm
from .models import Activity, ActivityPhoto
from users.models import Host


class ActivityDetailView(DetailView):
    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    form_class = ActivityUpdateForm
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."

    def test_func(self):
        activity = self.get_object()
        return activity.host.user == self.request.user
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


class ActivityPhotoUploadView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'activities/activity_upload.html'
    form_class = PhotoUploadForm

    def get_activity(self):
        return Activity.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        return self.get_activity().host.user == self.request.user

    def form_valid(self, form):
        max_photos = 5
        activity = self.get_activity()
        current_num_photos = ActivityPhoto.objects.filter(activity=activity).count()
        if (current_num_photos == max_photos):
            messages.error(self.request, _("You have reached your limit of 5 photos. \
                Please remove some to add photos."))
            return super().form_invalid(form)
        for image in form.cleaned_data['photos']:
            ActivityPhoto.objects.create(file=image, activity=activity)
            current_num_photos += 1
            if (current_num_photos == max_photos):
                messages.warning(self.request, _("Some photos were not uploaded because \
                    you have reached your photos limit."))
                break
        messages.success(self.request, _('Photo(s) successfully uploaded.'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('activities:upload', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    def get_context_data(self, **kwargs):
        activity = self.get_activity()
        context = super().get_context_data(**kwargs)
        context['activity'] = activity
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        return context


""" Template that corresponds to each step of the activity creation """
STEP_TEMPLATES = {
    "0": "activities/create/default.html",
    "1": "activities/create/default.html",
    "2": "activities/create/default.html",
    "3": "activities/create/default.html",
    "4": "activities/create/default.html",
    "5": "activities/create/location.html",
}


"""
    This is a multi-step form view for the activity creation.
    Each step will pass the data into the next step, until
    the form is finished. It is passed through SESSIONS.
"""
class ActivityCreationView(UserPassesTestMixin, SessionWizardView):

    """ Only users that are host can access the activity creation form """
    def test_func(self):
        host = Host.objects.filter(user=self.request.user)
        return self.request.user.is_authenticated and host

    def get_template_names(self):
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activities/activity_done.html', {
            'activity': instance,
        })
