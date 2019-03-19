from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from formtools.wizard.views import SessionWizardView
from .forms import ActivityForm
from .models import Activity
from users.models import Host


class ActivityDetailView(DetailView):
    template_name = 'activities/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


class ActivityUpdateView(SuccessMessageMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name_suffix = '_update'
    success_message = "Activity successfully updated."

    def get_object(self):
        host = Host.objects.get(user=self.request.user)
        return Activity.objects.get(host=host)
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()


# { "Name of step" : "The Form Step's template" }

STEP_TEMPLATES = {
    "0": "activities/create/default.html",
    "1": "activities/create/default.html",
    "2": "activities/create/default.html",
    "3": "activities/create/location.html",
}


class ActivityCreationView(UserPassesTestMixin, SessionWizardView):

    def test_func(self):
        host = Host.objects.filter(user=self.request.user)
        return self.request.user.is_authenticated and host

    def get_template_names(self):
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activities/activity_done.html', {
            'activity': instance,
        })
