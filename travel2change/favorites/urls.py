from django.urls import path
from .views import FavoritesListView, SetFavoritesView

app_name = 'favorites'
urlpatterns = [
    path('set/<int:pk>/', SetFavoritesView.as_view(), name='set'),
    path('', FavoritesListView.as_view(), name='list'),
]
