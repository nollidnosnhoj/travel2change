from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from users.models import Host
from users.mixins import UserIsHostViewMixin
from activities.models import Activity

User = get_user_model()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', ]
    template_name = "users/user_update.html"
    success_message = 'User Information Successfully Updated'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user_update')


""" Show host's profile """
class HostDetailView(DetailView):
    model = Host
    context_object_name = 'host'
    number_of_activites_in_profile = 5

    """ Add activity list into context """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = Activity.objects.filter(host=self.object)
        # Display 5 activities of the host's, ordered by the creation time
        context['activities'] = activities[:self.number_of_activites_in_profile]
        context['show_more_activities'] = activities.count() > self.number_of_activites_in_profile
        return context


""" Show host's profile update """
class HostUpdateView(LoginRequiredMixin, UserIsHostViewMixin, SuccessMessageMixin, UpdateView):
    model = Host
    fields = ['_name', 'custom_slug', 'description', 'phone', 'website']
    template_name_suffix = '_update'
    success_message = "Profile successfully updated."

    def get_object(self):
        return get_object_or_404(Host, user=self.request.user)
    
    """ Redirect user after successful update """
    def get_success_url(self):
        return reverse('host_detail', kwargs={'slug': self.object.slug})


class HostActivitiesListView(LoginRequiredMixin, ListView):
    model = Activity
    context_object_name = "activities"
    template_name = 'users/host_activities_list.html'

    def get_queryset(self):
        host = get_object_or_404(Host, user=self.request.user)
        return Activity.objects.approved().filter(host=host).order_by("-approved_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['host'] = get_object_or_404(Host, user=self.request.user)
        return context
