from django.conf.urls import url
from .forms import (
    RegionActivityForm, 
    TitleActivityForm, 
    AboutActivityForm,
    AddressActivityForm,
    LocationActivityForm,
    ImagesActivityForm,
)
from .views import ActivityDetailView, ActivityWizard

ACTIVITY_CREATE_STEP_FORMS = [
    ("01", RegionActivityForm),
    ("02", TitleActivityForm),
    ("03", AboutActivityForm),
    ("04", AddressActivityForm),
    ("05", LocationActivityForm),
    ("06", ImagesActivityForm),
]

urlpatterns = [
    url(r'^view/(?P<slug>[\w-]+)/$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^create/$', ActivityWizard.as_view(ACTIVITY_CREATE_STEP_FORMS), name="activity_wizard"),
]
