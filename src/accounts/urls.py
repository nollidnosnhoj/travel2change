from django.conf.urls import url
from django.conf.urls import include

from .views import (
    LoginView, RegisterView, logout_view
)

app_name = "accounts"
urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', logout_view),
    url(r'^register/', RegisterView.as_view()),
]