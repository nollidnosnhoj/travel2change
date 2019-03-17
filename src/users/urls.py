from django.urls import path
from .views import HostDetailView, HostUpdateView


urlpatterns = [
    path('hosts/<slug:slug>/', HostDetailView.as_view(), name="host_detail"),
    path('hosts/<slug:slug>/edit/', HostUpdateView.as_view(), name="host_update"),
]
