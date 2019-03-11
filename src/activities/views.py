from django.conf.global_settings import LOGIN_URL
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from formtools.wizard.views import SessionWizardView
from .forms import ActivityUpdateForm, ActivityImagesUpload
from .models import Activity, ActivityImage
from hosts.models import Host


""" Activity Detail View """
class ActivityDetailView(DetailView):
    template_name = 'activity/activity_detail.html'
    model = Activity
    context_object_name = 'activity'


""" Activity Update View """
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityUpdateForm
    template_name = 'activity/activity_update.html'
    message = _('Your activity has been updated.')

    def form_valid(self, form):
        host = Host.objects.get(user=self.request.user)
        form.instance.host = host
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('activities:detail')


""" Image Uploading View for an Activity """
class ActivityImageUploadView(UpdateView):
    model = Activity

    def get(self, request, *args, **kwargs):
        images = ActivityImage.objects.filter(host=self.object)
        return render(self.request, 'activity/activity_images_upload.html', {
            'images': images
        })
    
    def post(self, request, *args, **kwargs):
        form = ActivityImagesUpload(self.request.POST, self.request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.activity = self.object
            image.save()
            data = {
                'is_valid': True, 'name': image.file.name, 'url': image.file.url
            }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

# { "Name of step" : "The Form Step's template" }


STEP_TEMPLATES = {
    "0": "activity/create/default.html",
    "1": "activity/create/default.html",
    "2": "activity/create/default.html",
    "3": "activity/create/default.html",
    "4": "activity/create/default.html",
}


class ActivityWizard(SessionWizardView):

    def dispatch(self, request, *args, **kwargs):
        """ Redirect anonymous users to login page """
        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)
        """ Block non-host users access to activity creation """
        if not Host.objects.filter(user=request.user):
            return render(request, 'activity/activity_access_denied.html', {
                'user': request.user
            })
        return super().dispatch(request, *args, **kwargs)

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
