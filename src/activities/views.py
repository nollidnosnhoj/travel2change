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
    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        activity = self.get_object()
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        return context


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

    """ Get Activity object """
    def get_activity(self):
        return Activity.objects.get(pk=self.kwargs['pk'])

    """ Permission Testing """
    def test_func(self):
        return self.get_activity().host.user == self.request.user

    """ Form processing after form valid """
    def form_valid(self, form):
        # Maximum number of photos per activity
        max_photos = 5
        activity = self.get_activity()
        # Cache the current number of photos for the activity
        current_num_photos = ActivityPhoto.objects.filter(activity=activity).count()
        # Initially check if the current number of photos reached its max
        if (current_num_photos == max_photos):
            messages.error(self.request, _("You have reached your limit of 5 photos. \
                Please remove some to add photos."))
            return super().form_invalid(form)
        # Loop through each uploaded image, and create an object for each
        for image in form.cleaned_data['photos']:
            ActivityPhoto.objects.create(file=image, activity=activity)
            current_num_photos += 1  # Increment current number of photos
            # After creating photo object, check again.
            # If it's full, then stop uploading.
            if (current_num_photos == max_photos):
                messages.warning(self.request, _("Some photos were not uploaded because \
                    you have reached your photos limit."))
                return super().form_valid(form)
        messages.success(self.request, _('Photo(s) successfully uploaded.'))
        return super().form_valid(form)

    # Once photos are uploaded, redirect to the same page.
    def get_success_url(self):
        return reverse('activities:photos', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    # Display activity's photos
    def get_context_data(self, **kwargs):
        activity = self.get_activity()
        context = super().get_context_data(**kwargs)
        context['activity'] = activity
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        return context

# Delete photo
def photo_delete(request, pk):
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
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_photos'))

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
