from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Host
from activities.models import Activity


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
    fields = ['_name', 'description', 'phone', 'website']
    template_name_suffix = '_update'
    success_message = "Profile successfully updated."

    def test_func(self):
        host = self.get_object()
        return host.user == self.request.user
    
    """ Redirect user after successful update """
    def get_success_url(self):
        return self.get_object().get_absolute_url()
