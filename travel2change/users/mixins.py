from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from users.models import Host

class HostListView(ListView):
    def dispatch(self, request, *args, **kwargs):
        self.host = get_object_or_404(Host, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['host'] = self.host
        return context
