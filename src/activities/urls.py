from django.conf.urls import url

from .forms import ACTIVITY_CREATE_FORMS_LIST
from .views import ActivityDetailView, ActivityWizard

urlpatterns = [
    url(r'^view/(?P<slug>[\w-]+)/$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^create/$', ActivityWizard.as_view(ACTIVITY_CREATE_FORMS_LIST), name="activity_wizard"),
]
