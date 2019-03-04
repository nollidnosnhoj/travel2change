from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
# from django.shortcuts import render
from django.views.generic.detail import DetailView
from formtools.wizard.views import SessionWizardView
from .models import Activity


class ActivityDetailView(DetailView):
    template_name = 'activity/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


TEMPLATES = {
    "01": "activity/create/default.html",
    "02": "activity/create/default.html",
    "03": "activity/create/default.html",
    "04": "activity/create/default.html",
    "05": "activity/create/default.html",
    # "06": "activity/create/default.html",
}

"""
TODO:
- Handle multiple image uploading
- Handle Google Maps Geocoding
"""


class ActivityWizard(SessionWizardView, LoginRequiredMixin):

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Get merged dictionary from all form entries
        form_dict = self.get_all_cleaned_data()
        # Pop the m2m pair from dictionary
        activity_tags = form_dict.pop('tags')
        # Create activity instance based on user and form dictionary
        instance = Activity.objects.create(**form_dict, host=self.request.user)
        # Set m2m fields
        instance.tags.set(activity_tags)
        # Save instance into database
        instance.save()
        return HttpResponse("nice")
