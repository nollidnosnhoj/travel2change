from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from formtools.wizard.views import SessionWizardView
from .models import Activity
from hosts.models import Host


class ActivityDetailView(DetailView):
    template_name = 'activity/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


# { "Name of step" : "The Form Step's template" }

STEP_TEMPLATES = {
    "0": "activity/create/default.html",
    "1": "activity/create/default.html",
    "2": "activity/create/default.html",
    "3": "activity/create/location.html",
}


class ActivityWizard(UserPassesTestMixin, SessionWizardView):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_host

    def get_template_names(self):
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        host = Host.objects.get(user=self.request.user)
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        instance = Activity.objects.create(**form_dict, host=host)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activity/activity_done.html', {
            'activity': instance,
        })
