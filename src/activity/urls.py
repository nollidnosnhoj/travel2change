from django.conf.urls import url

from . import views
from .views import ActivityDetailView

urlpatterns = [
    url(
        r'^(?P<slug>[-\w]+)/$', 
        ActivityDetailView.as_view(),
        name='activity_detail'
    ),

]
