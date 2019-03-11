from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from .models import Host
from activities.models import Activity


class HostDetailView(DetailView):
    model = Host
    template_name = 'hosts/host_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(host=self.object)
        return context


class HostUpdateView(UpdateView):
    pass


class HostActivitiesListView(ListView):
    model = Activity
    template_name = 'hosts/host_activities_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(host=)
