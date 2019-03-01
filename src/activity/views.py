from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Activity

class ActivityDetailView(DetailView):
    template_name = 'activity/activity_detail.html'
    model = Activity
    context_object_name = 'activity'
