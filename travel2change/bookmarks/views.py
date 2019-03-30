from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from activities.models import Activity
from .models import Bookmark

class BookmarkListView(LoginRequiredMixin, ListView):
    template_name = "bookmarks/bookmark_list.html"
    context_object_name = 'bookmarks'
    paginate_by = 10
    ordering = ['-created']

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

def set_bookmark(request, **kwargs):
    pass
