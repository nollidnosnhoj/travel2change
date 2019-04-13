from django.urls import path
from .views import (
    UpdateReview,
    DeleteReview,
)

urlpatterns = [
    path('<int:pk>/update/', UpdateReview.as_view(), name="review_update"),
    path('<int:pk>/delete/', DeleteReview.as_view(), name="review_delete"),
]
