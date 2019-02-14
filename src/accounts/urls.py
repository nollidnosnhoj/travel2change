from django.conf.urls import url
from django.conf.urls import include

from .views import (
    LoginView, RegisterView, logout_view
)

app_name = "accounts"
urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
]