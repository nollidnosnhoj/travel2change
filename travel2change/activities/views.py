import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from formtools.wizard.views import SessionWizardView
from activities.forms import ActivityUpdateForm, PhotoUploadForm
from activities.models import Activity, Region, ActivityPhoto, Category, Tag
from activities.mixins import CanViewUnapproved, OwnershipViewOnly, HostOnlyView
from bookmarks.models import Bookmark
from users.models import Host

from django.views.generic import ListView

def is_valid_queryparam(param):
    return (param != '' and param is not None)

class ActivityBrowseView(ListView):
    model = Activity
    template_name = 'activities/activity_browse.html'
    paginate_by = 10
    context_object_name = 'activityBrowse'

    def get_queryset(self):
        qs = Activity.objects.all()

        title = self.request.GET.get('title')
        region = self.request.GET.get('region')
        categories = self.request.GET.get('categories')
        tags = self.request.GET.get('tags')

        if is_valid_queryparam(region) and region != 'All Regions':
            qs = qs.filter(region__name=region)
        if is_valid_queryparam(categories) and categories != 'All Categories':
            qs = qs.filter(categories__name=categories)
        if is_valid_queryparam(tags) and tags != 'All Tags':
            qs = qs.filter(tags__name__icontains=tags)
        if is_valid_queryparam(title):
            qs = qs.filter(title__icontains=title)
        
        return qs.order_by("approved_time")
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['regions'] = Region.objects.all()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class ActivityDetailView(CanViewUnapproved, DetailView):
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
        return reverse('host_detail', kwargs={
            'slug': self.get_object().host.slug,
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
