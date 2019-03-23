from django.conf.urls import url
from .forms import ACTIVITY_CREATE_FORMS_LIST
from .views import (
    ActivityDetailView,
    ActivityCreationView,
    ActivityUpdateView,
    ActivityPhotoUploadView,
    photo_delete,
)

app_name = 'activities'
urlpatterns = [
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/photos/', ActivityPhotoUploadView.as_view(), name='photos'),  # Photo upload URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/edit/', ActivityUpdateView.as_view(), name='update'),  # Activity Update URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>[0-9]+)/', ActivityDetailView.as_view(), name='detail'),  # Activity detail URL
    url(r'photos/delete/(?P<pk>[0-9]+)/', photo_delete, name="photo_delete"),  # Photo delete URL
    url(r'^create/', ActivityCreationView.as_view(ACTIVITY_CREATE_FORMS_LIST), name="create"),  # Activity Create URL
]
