# from django.shortcuts import render
# from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Host
from activities.models import Activity


""" Show host's profile """
class HostDetailView(DetailView):
    model = Host
    template_name = 'hosts/host_detail.html'
    context_object_name = 'host'

    """ Add activity list into context """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Display 5 activities of the host's, ordered by the creation time
        context['activities'] = Activity.objects.filter(host=self.object)[:5]
        return context


""" Show host's profile update """
class HostUpdateView(UpdateView):
    model = Host
    fields = ['_name', 'description', 'phone', 'website']
    template_name_suffix = '_update'

    """ Get the profile associated with the current user's host """
    def get_object(self):
        return Host.objects.get(user=self.request.user)
    
    """ Redirect user after successful update """
    def get_success_url(self):
        return self.get_object().get_absolute_url()
