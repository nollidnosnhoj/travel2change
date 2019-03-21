from django.conf.urls import url
from .forms import ACTIVITY_CREATE_FORMS_LIST
from .views import (
    ActivityDetailView,
    ActivityCreationView,
    ActivityUpdateView,
)

app_name = 'activities'
urlpatterns = [
    url(
        r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/edit/',
        ActivityUpdateView.as_view(),
        name='update',
    ),
    url(
        r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/',
        ActivityDetailView.as_view(),
        name='detail',
    ),
    url(r'^create/', ActivityCreationView.as_view(ACTIVITY_CREATE_FORMS_LIST), name="create"),
]
