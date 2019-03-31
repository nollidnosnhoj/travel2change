from django.urls import path
from bookmarks.views import BookmarkListView, SetBookmarkView

app_name = 'bookmarks'
urlpatterns = [
    path('set/<int:pk>/', SetBookmarkView.as_view(), name='set'),
    path('', BookmarkListView.as_view(), name='list'),
]
