import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, FormView, UpdateView
from formtools.wizard.views import SessionWizardView
from activities.forms import PhotoUploadForm
from activities.mixins import CanViewUnapprovedMixin, OwnerViewOnlyMixin, HostViewOnlyMixin
from activities.models import Activity, ActivityPhoto
from bookmarks.models import Bookmark
from users.models import Host


class ActivityDetailView(CanViewUnapprovedMixin, DetailView):
    """ View for showing the details of the activity """

    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.filter(activity=self.object)
        if self.request.user.is_authenticated:
            context['bookmarked'] = Bookmark.objects.filter(user=self.request.user, activity=self.get_object()).exists()
        return context


class ActivityDeleteView(LoginRequiredMixin, OwnerViewOnlyMixin, SuccessMessageMixin, DeleteView):
    template_name = "activities/activity_delete.html"
    success_message = "Activity successfully deleted."

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('host_detail', kwargs={
            'slug': self.get_object().host.slug,
        })


class ActivityUpdateView(LoginRequiredMixin, OwnerViewOnlyMixin, UpdateView):
    model = Activity
    fields = (
        'title',
        'region',
        'description',
        'highlights',
        'requirements',
        'categories',
        'tags',
        'featured_photo',
        'price',
        'address',
        'latitude',
        'longitude',
        'fh_item_id',
    )
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


class ActivityPhotoUploadView(LoginRequiredMixin, OwnerViewOnlyMixin, FormView):
    template_name = 'activities/activity_upload.html'
    form_class = PhotoUploadForm
    max_photos = settings.MAX_PHOTOS_PER_ACTIVITY

    def dispatch(self, request, *args, **kwargs):
        """ Get the current activity """
        self.activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Upload the photos for the activities
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('photos')
        # Count the number of activity photos for the activity. The number is cached.
        current_num = ActivityPhoto.objects.filter(activity=self.activity).count()
        if form.is_valid():
            for f in files:
                # Thrown an error if the photos reached the limit
                if (current_num == self.max_photos):
                    messages.error(self.request, "You have reached your photos limit.")
                    return self.form_invalid(form)
                else:
                    # Create new activity photo and increment count
                    instance = ActivityPhoto(file=f, activity=self.activity)
                    instance.save()
                    current_num += 1
            messages.success(self.request, "Photo(s) successfully uploaded.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('activities:photos', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = self.activity
        context['photos'] = ActivityPhoto.objects.filter(activity=self.activity)
        context['max_photos'] = self.max_photos
        return context


def photo_delete(request, pk):
    """ Simple view to delete photo """
    photo = get_object_or_404(ActivityPhoto, pk=pk)
    photo.file.delete(False)
    photo.delete()
    return HttpResponse("Photo deleted successfully.")


class ActivityCreationView(LoginRequiredMixin, HostViewOnlyMixin, SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_photos'))
    STEP_TEMPLATES = {
        "0": "activities/wizard_templates/default.html",
        "1": "activities/wizard_templates/default.html",
        "2": "activities/wizard_templates/default.html",
        "3": "activities/wizard_templates/default.html",
        "4": "activities/wizard_templates/price_fh.html",
        "5": "activities/wizard_templates/location.html",
        "6": "activities/wizard_templates/featured_photo.html",
        "7": "activities/wizard_templates/confirmation.html",
    }

    def get_template_names(self):
        """ Grab dictionary of templates for wizard """
        return [self.STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Call when the wizard is completed.
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        activity_categories = form_dict.pop('categories')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.categories.set(activity_categories)
        instance.tags.set(activity_tags)
        instance.save()
        return render(
            self.request,
            'activities/activity_done.html',
            {'activity': instance, }
        )
