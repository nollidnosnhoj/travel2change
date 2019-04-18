from django.urls import path
from users.views import (
    HostReviewsListView,
    HostActivitiesPublicListView,
    HostActivitiesDashboardView,
    HostDetailView,
    HostUpdateView,
    UserUpdateView,
    UserReviewsListView,
)


urlpatterns = [
    path('hosts/<slug:slug>/reviews/', HostReviewsListView.as_view(), name='host_reviews'),
    path('hosts/<slug:slug>/activities/', HostActivitiesPublicListView.as_view(), name="host_activities"),
    path('hosts/<slug:slug>/', HostDetailView.as_view(), name="host_detail"),
    path('accounts/reviews/', UserReviewsListView.as_view(), name="user_reviews"),
    path('accounts/host/activities/', HostActivitiesDashboardView.as_view(), name="host_activities_dashboard"),
    path('accounts/host/', HostUpdateView.as_view(), name="host_update"),
    path('accounts/', UserUpdateView.as_view(), name='user_update'),
]
