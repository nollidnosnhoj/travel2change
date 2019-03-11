from django.conf.urls import url

from .forms import ACTIVITY_CREATE_FORMS_LIST
from .views import (
    ActivityDetailView, ActivityUpdateView, ActivityImageUploadView, ActivityWizard
)

urlpatterns = [
    url(
        r'^view/(?P<slug>[\w-]+)/$', ActivityDetailView.as_view(), name='detail'
    ),
    url(
        r'^update/(?P<pk>\d+)/$', ActivityUpdateView.as_view(), name='update'
    ),
    url(
        r'^update/image-upload/(?P<pk>\d+)/$', ActivityImageUploadView.as_view(), name='images_upload'
    ),
    url(
        r'^create/$', ActivityWizard.as_view(ACTIVITY_CREATE_FORMS_LIST), name="create"
    ),
]
