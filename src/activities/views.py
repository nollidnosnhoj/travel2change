import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from formtools.wizard.views import SessionWizardView
from .forms import ActivityUpdateForm, PhotoUploadForm
from .models import Activity, ActivityPhoto
from users.models import Host


class ActivityDetailView(DetailView):
    """ View for showing the details of the activity """

    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        """ Show activity's photo """
        activity = self.get_object()
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        return context


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """ View for updating activity """

    model = Activity
    form_class = ActivityUpdateForm
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."

    def test_func(self):
        """ Validate if the user is the host of the activity """
        return self.get_object().host.user == self.request.user
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


class ActivityPhotoUploadView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """ View for uploading photos for a specific activity """

    template_name = 'activities/activity_upload.html'
    form_class = PhotoUploadForm

    def get_activity(self):
        """ Get activity from url """
        return Activity.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        """ Validate if current user is the host of the activity """
        return self.get_activity().host.user == self.request.user

    def form_valid(self, form):
        """
        When a form is valid, validate for limits and create Photo objects for the activity.
        """
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
                return super().form_valid(form)
        messages.success(self.request, _('Photo(s) successfully uploaded.'))
        return super().form_valid(form)

    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:photos', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    def get_context_data(self, **kwargs):
        """ Display activity's photos """
        activity = self.get_activity()
        context = super().get_context_data(**kwargs)
        context['activity'] = activity
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        return context

def photo_delete(request, pk):
    """ Function for deleting an activity's photo """
    photo = get_object_or_404(ActivityPhoto, pk=pk)
    photo.delete()
    return JsonResponse({'message': 'Successful!'})


""" Template that corresponds to each step of the activity creation """
STEP_TEMPLATES = {
    "0": "activities/wizard_templates/default.html",
    "1": "activities/wizard_templates/default.html",
    "2": "activities/wizard_templates/default.html",
    "3": "activities/wizard_templates/default.html",
    "4": "activities/wizard_templates/default.html",
    "5": "activities/wizard_templates/location.html",
    "6": "activities/wizard_templates/featured_photo.html",
}


class ActivityCreationView(UserPassesTestMixin, SessionWizardView):
    """ View for activity creation wizard """

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_photos'))

    def test_func(self):
        """ Check if user is a host """
        host = Host.objects.filter(user=self.request.user)
        return self.request.user.is_authenticated and host

    def get_template_names(self):
        """ Grab dictionary of templates for wizard """
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """ Calls function after the wizard is completed. Create activity after done """
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activities/activity_done.html', {
            'activity': instance,
        })
