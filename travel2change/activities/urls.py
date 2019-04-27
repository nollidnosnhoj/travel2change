from django.conf.urls import url
from activities.forms import ACTIVITY_CREATE_FORMS_LIST
from activities.views import (
    ActivityBrowseView,
    ActivityBrowseRegionView,
    ActivityDetailView,
    ActivityCreationView,
    ActivityUpdateView,
    ActivityPhotoUploadView,
    ActivityDeleteView,
    photo_delete,
)

activity_creation = ActivityCreationView.as_view(
    ACTIVITY_CREATE_FORMS_LIST,
    url_name='activities:create_step',
    done_step_name='complete',
)

app_name = 'activities'
urlpatterns = [
    url(r'^create/(?P<step>.+)/', activity_creation, name='create_step'),
    url(r'^create/', activity_creation, name="create"),  # Activity Create URL
    url(r'photos/delete/(?P<pk>[0-9]+)/', photo_delete, name="photo_delete"),  # Photo delete URL
    url(r'delete/(?P<pk>\d+)/', ActivityDeleteView.as_view(), name='delete'),  # Activity Delete URL
    url(r'photos/(?P<pk>\d+)/', ActivityPhotoUploadView.as_view(), name='photos'),  # Photo upload URL
    url(r'update/(?P<pk>\d+)/', ActivityUpdateView.as_view(), name='update'),  # Activity Update URL
    url(r'(?P<region>[\w-]+)/(?P<slug>[\w-]+)/', ActivityDetailView.as_view(), name='detail'),  # Activity detail URL
    url(r'(?P<region>[\w-]+)/', ActivityBrowseRegionView.as_view(), name="browse_region"),
    url(r'^', ActivityBrowseView.as_view(), name="browse"),
]
