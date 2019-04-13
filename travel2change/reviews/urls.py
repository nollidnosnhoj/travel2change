from django.urls import path
from .views import UpdateReview

urlpatterns = [
    path('<int:pk>/update/', UpdateReview.as_view(), name="review_update"),
]
