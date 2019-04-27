import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.views.generic.edit import FormMixin
from formtools.wizard.views import NamedUrlSessionWizardView
from favorites.models import Favorite
from reviews.forms import ReviewForm
from reviews.models import Review
from users.models import Host
from points.models import award_points
from .forms import PhotoUploadForm
from .mixins import UnapprovedActivityMixin, ReviewCheck
from .models import Activity, ActivityPhoto, Region, Category, Tag

def is_valid_queryparam(param):
    return (param != '' and param is not None)


class BrowseView(ListView):
    model = Activity
    template_name = 'activities/activity_browse.html'
    paginate_by = 10
    context_object_name = 'activityBrowse'

    def dispatch(self, request, *args, **kwargs):
        self.q = None
        self.title = None
        self.categories = None
        self.tags = None
        self.price = None
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Activity.objects.select_related('host__user').select_related('region').approved()

        if self.region:
            qs = qs.filter(region__slug=self.region)

        self.q = self.request.GET.get('q')
        self.title = self.request.GET.get('title')
        self.categories = self.request.GET.get('categories')
        self.tags = self.request.GET.getlist('tags')
        self.price = self.request.GET.get('price')

        if is_valid_queryparam(self.q):
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=self.q) | Q(region__slug=self.q) | Q(categories__slug=self.q) | Q(tags__slug=self.q)
            ).distinct()

        if is_valid_queryparam(self.categories):
            qs = qs.filter(categories__slug=self.categories)

        if is_valid_queryparam(self.tags) and self.tags:
            for tag in self.tags:
                qs = qs.filter(tags__slug=self.tag).distinct()

        if is_valid_queryparam(self.title):
            qs = qs.filter(title__icontains=self.title)
        
        if is_valid_queryparam(self.price):
            if self.price == 'free':
                qs = qs.filter(price__exact=0)
            if self.price == 'paid':
                qs = qs.filter(price__gt=0)
        
        return qs.order_by("-is_featured")
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['regions'] = Region.objects.all()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        try:
            context['current_region'] = Region.objects.get(slug=self.region)
        except Region.DoesNotExist:
            context['current_region'] = 'All Regions'
        return context


class ActivityBrowseRegionView(BrowseView):
    def dispatch(self, request, *args, **kwargs):
        self.region = self.kwargs['region']
        return super().dispatch(request, *args, **kwargs)


class ActivityBrowseView(BrowseView):
    def dispatch(self, request, *args, **kwargs):
        self.region = None
        return super().dispatch(request, *args, **kwargs)


class ActivityDetailView(UnapprovedActivityMixin, ReviewCheck, FormMixin, DetailView):
    """ View for showing the details of the activity """
 
    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'
    form_class = ReviewForm
 
    def dispatch(self, request, *args, **kwargs):
        # Get activity object
        self.object = self.get_object()
        if not self.object.is_approved:
            messages.warning(request, "This activity is currently not published, and awaiting approval.")
        self.can_review = self.has_review_permission(request)
        return super().dispatch(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = ActivityPhoto.objects.select_related('activity').filter(activity=self.object)
        context['reviews'] = Review.objects.select_related('activity').filter(activity=self.object).order_by('-created')
        context['can_review'] = self.can_review
        if self.request.user.is_authenticated:
            context['favorited'] = Favorite.objects.filter(user=self.request.user, activity=self.object).exists()
        return context
   
    def get_object(self):
        return self.model.objects.select_related('host__user').get(region__slug=self.kwargs['region'], slug=self.kwargs['slug'])
   
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
        if new_review.photo:
            award_points(new_review.user, 'review_photo')
        award_points(new_review.user, 'review_create')
        new_review.save()
        self.object.review_count += 1
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Review cannot be submitted. Please check for validation errors.")
        return super().form_invalid(form)
   
    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:detail', kwargs={
            'region': self.kwargs['region'],
            'slug': self.kwargs['slug'],
        })


class ActivityDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "activities/activity_delete.html"
    success_message = "Activity successfully deleted."

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'], host=self.request.user.host)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """ Redirect to activity's photos page after successful upload """
        return reverse('activities:photos', kwargs={
            'pk': self.kwargs['pk'],
        })


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
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
    )
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."

    def get_object(self):
        return get_object_or_404(Activity, pk=self.kwargs['pk'], host=self.request.user.host)

    def form_invalid(self, form):
        messages.error(self.request, "Activity cannot be updated. Please check for validation errors.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


class ActivityPhotoUploadView(LoginRequiredMixin, FormView):
    template_name = 'activities/activity_upload.html'
    form_class = PhotoUploadForm
    max_photos = settings.MAX_PHOTOS_PER_ACTIVITY

    def dispatch(self, request, *args, **kwargs):
        """ Get the current activity """
        self.activity = get_object_or_404(Activity, pk=self.kwargs['pk'], host=self.request.user.host)
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
            messages.error(self.request, "You must only upload images (jpg|gif|png).")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('activities:photos', kwargs={
            'pk': self.kwargs['pk'],
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = self.activity
        context['photos'] = ActivityPhoto.objects.select_related('activity').filter(activity=self.activity)
        context['max_photos'] = self.max_photos
        return context


def photo_delete(request, pk):
    """ Simple view to delete photo """
    photo = get_object_or_404(ActivityPhoto, pk=pk)
    photo.delete()
    return HttpResponse("Photo deleted successfully.")


class ActivityCreationView(LoginRequiredMixin, UserPassesTestMixin, NamedUrlSessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_photos'))
    permission_denied_message = "You must be a host to view page."

    STEP_TEMPLATES = {
        "1": "activities/wizard_templates/default.html",
        "2": "activities/wizard_templates/default.html",
        "3": "activities/wizard_templates/default.html",
        "4": "activities/wizard_templates/default.html",
        "5": "activities/wizard_templates/price_fh.html",
        "6": "activities/wizard_templates/location.html",
        "7": "activities/wizard_templates/featured_photo.html",
        "8": "activities/wizard_templates/confirmation.html",
    }

    def test_func(self):
        return Host.objects.filter(user=self.request.user).exists()

    def get_template_names(self):
        """ Grab dictionary of templates for wizard """
        return [self.STEP_TEMPLATES[self.steps.current]]
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_data'] = self.get_all_cleaned_data()
        return context

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
