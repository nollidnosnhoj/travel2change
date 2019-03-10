from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from formtools.wizard.views import SessionWizardView
from .models import Activity


class ActivityDetailView(DetailView):
    template_name = 'activity/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


# { "Name of step" : "The Form Step's template" }

STEP_TEMPLATES = {
    "0": "activity/create/default.html",
    "1": "activity/create/default.html",
    "2": "activity/create/default.html",
    "3": "activity/create/default.html",
    "4": "activity/create/default.html",
}


class ActivityWizard(LoginRequiredMixin, SessionWizardView):

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_template_names(self):
        return [STEP_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        form_dict = self.get_all_cleaned_data()
        activity_tags = form_dict.pop('tags')
        instance = Activity.objects.create(**form_dict, host=self.request.host)
        instance.tags.set(activity_tags)
        instance.save()
        
        return render(self.request, 'activity/activity_done.html', {
            'activity': instance,
        })
