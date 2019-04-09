import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.urls import reverse
from django.views.generic import (
    DetailView,
    FormView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormMixin
from formtools.wizard.views import SessionWizardView
from activities.forms import (
    ActivityUpdateForm,
    PhotoUploadForm
)
from activities.mixins import (
    CanViewUnapproved,
    OwnershipViewOnly,
    HostOnlyView
)
from activities.models import (
    Activity,
    ActivityPhoto,
)
from bookmarks.models import Bookmark
from reviews.forms import ReviewForm
from reviews.models import ActivityReview
from users.models import Host


class ActivityDetailView(CanViewUnapproved, FormMixin, DetailView):
    """ View for showing the details of the activity """

    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'
    form_class = ReviewForm

    def dispatch(self, request, *args, **kwargs):
        # Get activity object
        self.object = self.get_object()
        # Check if the user can review the activity
        self.can_review = self.check_if_user_can_review()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.filter(activity=self.object)
        context['reviews'] = ActivityReview.objects.filter(activity=self.object)
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm(initial={'activity': self.object})
            context['can_review'] = self.can_review
            context['bookmarked'] = Bookmark.objects.filter(user=self.request.user, activity=self.object).exists()
        return context
    
    # process review form
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and self.can_review:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    # save review after form valid
    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.user = self.request.user
        new_review.activity = self.object
        new_review.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:detail', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    def check_if_user_can_review(self):
        if self.request.user.is_authenticated and self.object.status == 'approved':
            return ActivityReview.objects.filter(user=self.request.user, activity=self.object).count() < 1
        else:
            return False


class ActivityDeleteView(LoginRequiredMixin, OwnershipViewOnly, SuccessMessageMixin, DeleteView):
    template_name = "activities/activity_delete.html"
    success_message = "Activity successfully deleted."

    def get_object(self):
        # Get the object that corresponds to the primary key
        return get_object_or_404(Activity, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:photos', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })


class ActivityUpdateView(LoginRequiredMixin, OwnershipViewOnly, UpdateView):
    """ View for updating activity """

    model = Activity
    form_class = ActivityUpdateForm
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


class ActivityPhotoUploadView(LoginRequiredMixin, OwnershipViewOnly, FormView):
    template_name = 'activities/activity_upload.html'
    form_class = PhotoUploadForm
    max_photos = settings.MAX_PHOTOS_PER_ACTIVITY

    def dispatch(self, request, *args, **kwargs):
        self.activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Upload the photos for the activities
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('photos')
        current_num = ActivityPhoto.objects.filter(activity=self.activity).count()
        if form.is_valid():
            for f in files:
                if (current_num == self.max_photos):
                    messages.error(self.request, "You have reached your photos limit.")
                    return self.form_invalid(form)
                else:
                    instance = ActivityPhoto(file=f, activity=self.activity)
                    instance.save()
                    current_num += 1
            messages.success(self.request, "Photo(s) successfully uploaded.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:photos', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
            'pk': self.kwargs['pk']
        })
    
    def get_context_data(self, **kwargs):
        """ Display activity's photos """
        context = super().get_context_data(**kwargs)
        context['activity'] = self.activity
        context['photos'] = ActivityPhoto.objects.filter(activity=self.activity)
        context['max_photos'] = self.max_photos
        return context


def photo_delete(request, pk):
    """ Function for deleting an activity's photo """
    photo = get_object_or_404(ActivityPhoto, pk=pk)
    photo.file.delete(False)
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


class ActivityCreationView(LoginRequiredMixin, HostOnlyView, SessionWizardView):
    """ View for activity creation wizard """

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_photos'))

    def get_template_names(self):
        """ Grab dictionary of templates for wizard """
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """ Calls function after the wizard is completed. Create activity after done """
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        activity_categories = form_dict.pop('categories')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.categories.set(activity_categories)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activities/activity_done.html', {
            'activity': instance,
        })
