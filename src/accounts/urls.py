from django.conf.urls import url

from .views import (
    LoginView, RegisterView, logout_view, 
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
)

app_name = "accounts"
urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),

    url(r'^password_reset/$', CustomPasswordResetView.as_view(), name="password_reset"),
    url(r'^password_reset/done/$', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        CustomPasswordResetConfirmView.as_view(), name='passowrd_reset_confirm'
    ),
    url(r'^reset/done/$', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete")
]