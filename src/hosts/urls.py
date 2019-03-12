from django.conf.urls import url
from django.urls import path
from .views import HostDetailView, HostUpdateView

app_name = 'hosts'
urlpatterns = [
    path('<int:pk>/', HostDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', HostUpdateView.as_view(), name='update')
]
