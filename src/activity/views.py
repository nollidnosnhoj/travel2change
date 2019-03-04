from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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
    "06": "activity/create/default.html",
}

class ActivityWizard(SessionWizardView, LoginRequiredMixin):
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list]
        })

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)
