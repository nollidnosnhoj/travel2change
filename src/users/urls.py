from django.urls import path
from .views import HostDetailView, HostUpdateView


urlpatterns = [
    path('hosts/<int:pk>/', HostDetailView.as_view(), name="host_detail"),
    path('hosts/<int:pk>/update/', HostUpdateView.as_view(), name="host_update"),
]
