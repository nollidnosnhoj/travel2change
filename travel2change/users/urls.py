from django.urls import path
from users.views import (
    HostActivitiesListView,
    HostDetailView,
    HostUpdateView,
    UserUpdateView,
)


urlpatterns = [
    path('hosts/<slug:slug>/activities/', HostActivitiesListView.as_view(), name="host_activities"),
    path('hosts/<slug:slug>/edit/', HostUpdateView.as_view(), name="host_update"),
    path('hosts/<slug:slug>/', HostDetailView.as_view(), name="host_detail"),
    path('users/edit/', UserUpdateView.as_view(), name='user_update'),
]
