from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from activities.models import Activity
from .models import Bookmark

class BookmarkListView(LoginRequiredMixin, ListView):
    template_name = "bookmarks/bookmarks_list.html"
    context_object_name = 'bookmarks'
    paginate_by = 12

    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(user=self.request.user)
        return bookmarks.select_related('activity').all().order_by('-created')


class SetBookmarkView(LoginRequiredMixin, View):
    model = Bookmark

    def post(self, request, pk):
        user = get_user(request)
        activity = get_object_or_404(Activity, pk=pk)
        bookmark, created = self.model.objects.get_or_create(
            user=user, activity=activity,)
        if not created:
            bookmark.delete()
        success_add = 'You have bookmarked this activity.'
        success_delete = 'You have removed this bookmark.'
        return JsonResponse({
            'result': 1 if created else 0,
            'message': success_add if created else success_delete
        })
