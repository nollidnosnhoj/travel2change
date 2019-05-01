from django.urls import path
from allauth.account.views import LoginView
from axes.decorators import axes_dispatch
from axes.decorators import axes_form_invalid
from django.utils.decorators import method_decorator
from users.forms import LoginForm
from users.views import (
    HostReviewsListView,
    HostActivitiesListView,
    HostAccountActivitiesListView,
    HostDetailView,
    HostUpdateView,
    UserUpdateView,
    UserReviewsListView,
)

LoginView.dispatch = method_decorator(axes_dispatch)(LoginView.dispatch)
LoginView.form_invalid = method_decorator(axes_form_invalid)(LoginView.form_invalid)


urlpatterns = [
    path('hosts/<slug:slug>/reviews/', HostReviewsListView.as_view(), name='host_reviews'),
    path('hosts/<slug:slug>/activities/', HostActivitiesListView.as_view(), name="host_activities"),
    path('hosts/<slug:slug>/', HostDetailView.as_view(), name="host_detail"),
    path('accounts/reviews/', UserReviewsListView.as_view(), name="user_reviews"),
    path('accounts/host/activities/', HostAccountActivitiesListView.as_view(), name="host_activities_dashboard"),
    path('accounts/host/', HostUpdateView.as_view(), name="host_update"),
    path('accounts/login/', LoginView.as_view(form_class=LoginForm), name='account_login'),
    path('accounts/', UserUpdateView.as_view(), name='user_update'),
]
