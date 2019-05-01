from django. contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from users.models import Host
from users.mixins import HostListView
from activities.models import Activity
from reviews.models import Review

User = get_user_model()

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', ]
    template_name = "users/user_update.html"
    context_object_name = "user"
    success_message = 'User Information Successfully Updated'

    def get_object(self):
        return self.request.user
    
    def form_invalid(self, form):
        messages.error(self.request, "User Info. unable to update. Please check for validation errors.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('user_update')


class UserReviewsListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Review
    context_object_name = "reviews"
    template_name = "users/user_reviews.html"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class HostDetailView(DetailView):
    model = Host
    context_object_name = 'host'
    number_of_activites_in_profile = 8
    number_of_reviews_in_profile = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = Activity.objects.select_related('region').select_related('host__user').approved().filter(host=self.object).order_by('-created')
        reviews = Review.objects.select_related('activity__host').filter(activity__in=activities)
        context['activities'] = activities[:self.number_of_activites_in_profile]
        context['reviews'] = reviews[:self.number_of_reviews_in_profile]
        return context


class HostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Host
    fields = [
        '_name',
        'custom_slug',
        'description',
        'contact_email',
        'phone',
        'website',
        'fh_username',
    ]
    template_name_suffix = '_update'
    success_message = "Profile successfully updated."

    def get_object(self):
        return get_object_or_404(Host, user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request, "Profile unable to update. Please check for validation errors.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('host_detail', kwargs={'slug': self.object.slug})


class HostActivitiesListView(HostListView):
    model = Activity
    context_object_name = "activities"
    template_name = 'users/host_activities_list.html'

    def get_queryset(self):
        return Activity.objects.select_related('host__user').select_related('region').approved().filter(host=self.host).order_by("-created")


class HostAccountActivitiesListView(DetailView):
    model = Host
    template_name = "users/host_activities_dashboard.html"

    def get_object(self):
        return get_object_or_404(Host, user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['activities'] = Activity.objects.select_related('host__user').select_related('region').all().filter(host=self.object).distinct().order_by('-status', '-created')
        return context


class HostReviewsListView(HostListView):
    model = Review
    context_object_name = "reviews"
    template_name = 'users/host_reviews_list.html'
    
    def get_queryset(self):
        activities = list(Activity.objects.approved().filter(host=self.host).values_list('pk', flat=True))
        reviews = Review.objects.select_related('activity__host').filter(activity__in=activities)
        return reviews
