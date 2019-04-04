import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from formtools.wizard.views import SessionWizardView
from activities.forms import ActivityUpdateForm, PhotoUploadForm
from activities.models import Activity, ActivityPhoto
from bookmarks.models import Bookmark
from users.models import Host

from django.views.generic import ListView

class ActivityBrowseView(ListView):
    model = Activity
    template_name = 'activities/activity_browse.html'
    paginate_by = 10
    def get_queryset(self):
        # query all activities
        qs = Activity.approved.all()
        
        # Get value from the filter form
        title = self.request.GET.get('title')
        region = self.request.GET.getlist('region')
        categories = self.request.GET.getlist('categories')
        tags = self.request.GET.getlist('tags')
        sort_by = self.request.GET.get('sortby')
        
        # filter activities if the query is present
        if not region:
            qs = qs.filter(region__in=region)
        if not categories:
            qs = qs.filter(categories__in=categories)
        if not tags:
            qs = qs.filter(tags__in=tags)
        if title != '':
            qs = qs.filter(title__icontains=title)
            
        # sort the query by the sortby value
        qs = qs.order_by(sort_by)
        
        return qs

class ActivityDetailView(DetailView):
    """ View for showing the details of the activity """

    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        """ Show activity's photo """
        current_user = get_user(self.request)
        activity = self.get_object()
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
        context['bookmarked'] = Bookmark.objects.filter(user=current_user, activity=activity).exists()
        return context


class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    template_name = "activities/activity_delete.html"
    success_message = "Activity successfully deleted."

    def test_func(self):
        """ Validate if the user is the host of the activity """
        return self.get_object().host.user == self.request.user

    def get_object(self):
        activity_id = self.kwargs['pk']
        return get_object_or_404(Activity, pk=activity_id)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('host_detail', kwargs={
            'slug': self.get_object().host.slug,
        })


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
    max_photos = 5

    def get_activity(self):
        """ Get activity from url """
        return Activity.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        """ Validate if current user is the host of the activity """
        return self.get_activity().host.user == self.request.user

    def post(self, request, *args, **kwargs):
        activity = self.get_activity()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('photos')
        current_num = ActivityPhoto.objects.filter(activity=activity).count()
        if form.is_valid():
            for f in files:
                if (current_num == self.max_photos):
                    messages.error(self.request, "You have reached your photos limit.")
                    return self.form_invalid(form)
                else:
                    instance = ActivityPhoto(file=f, activity=activity)
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
        activity = self.get_activity()
        context = super().get_context_data(**kwargs)
        context['activity'] = activity
        context['photos'] = ActivityPhoto.objects.filter(activity=activity)
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
        activity_categories = form_dict.pop('categories')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.categories.set(activity_categories)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activities/activity_done.html', {
            'activity': instance,
        })
