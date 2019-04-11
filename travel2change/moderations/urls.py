from django.urls import path
from .views import ModerationActivityQueue, ActivityApprovalView, ActivityDisapprovalView

app_name = 'moderations'
urlpatterns = [
    path('', ModerationActivityQueue.as_view(), name="queue"),
    path('<int:pk>/approve/', ActivityApprovalView.as_view(), name="approve"),
    path('<int:pk>/disapprove/', ActivityDisapprovalView.as_view(), name="disapprove"),
]
