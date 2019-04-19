from django.conf.urls import url
from activities.forms import ACTIVITY_CREATE_FORMS_LIST
from activities.views import (
    ActivityBrowseView,
    ActivityDetailView,
    ActivityCreationView,
    ActivityUpdateView,
    ActivityPhotoUploadView,
    ActivityDeleteView,
    photo_delete,
)

app_name = 'activities'
urlpatterns = [
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)/delete/', ActivityDeleteView.as_view(), name='delete'),  # Activity Delete URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)/photos/', ActivityPhotoUploadView.as_view(), name='photos'),  # Photo upload URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)/edit/', ActivityUpdateView.as_view(), name='update'),  # Activity Update URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)/', ActivityDetailView.as_view(), name='detail'),  # Activity detail URL
    url(r'photos/delete/(?P<pk>[0-9]+)/', photo_delete, name="photo_delete"),  # Photo delete URL
    url(r'^create/', ActivityCreationView.as_view(ACTIVITY_CREATE_FORMS_LIST), name="create"),  # Activity Create URL
    url(r'^', ActivityBrowseView.as_view(), name="browse"),
]
