from django.urls import path
from users.views import (
    HostActivitiesListView,
    HostDetailView,
    HostUpdateView,
    UserUpdateView,
)


urlpatterns = [
    path('hosts/<slug:slug>/activities/', HostActivitiesListView.as_view(), name="host_activities"),
    path('hosts/<slug:slug>/', HostDetailView.as_view(), name="host_detail"),
    path('accounts/host/', HostUpdateView.as_view(), name="host_update"),
    path('accounts/', UserUpdateView.as_view(), name='user_update'),
]
