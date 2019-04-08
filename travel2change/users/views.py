from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from users.models import Host
from activities.models import Activity

User = get_user_model()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', ]
    template_name_suffix = '_update'
    success_message = 'User Information Successfully Updated'

    def get_success_url(self):
        return reverse('user_update')


""" Show host's profile """
class HostDetailView(DetailView):
    model = Host
    context_object_name = 'host'

    """ Add activity list into context """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Display 5 activities of the host's, ordered by the creation time
        context['activities'] = Activity.objects.filter(host=self.object)[:5]
        return context


""" Show host's profile update """
class HostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Host
    fields = ['_name', 'custom_slug', 'description', 'phone', 'website', 'fh_username', ]
    template_name_suffix = '_update'
    success_message = "Profile successfully updated."

    def test_func(self):
        host = self.get_object()
        return host.user == self.request.user
    
    """ Redirect user after successful update """
    def get_success_url(self):
        return reverse('host_detail', kwargs={'slug': self.object.slug})
