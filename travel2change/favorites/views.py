from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from activities.models import Activity
from .models import Favorite

class FavoritesListView(LoginRequiredMixin, ListView):
    template_name = "favorites/favorites_list.html"
    context_object_name = 'favorites'

    def get_queryset(self):
        favorites = Favorite.objects.filter(user=self.request.user)
        return favorites.select_related('activity').all().order_by('-created')


class SetFavoritesView(View):
    """
    This will either create or delete favorite object, based on whether it exists or not.
    """
    model = Favorite
    
    def post(self, request, pk):
        if request.user.is_authenticated:
            activity = get_object_or_404(Activity, pk=pk)
            favorite, created = self.model.objects.get_or_create(
                user=request.user, activity=activity,
            )
            if not created:
                cooldown_time = favorite.created + timedelta(minutes=settings.FAVORITE_COOLDOWN_IN_MINUTES)
                if (cooldown_time >= datetime.now()):
                    favorite.delete()
                else:
                    remaining_time = datetime.now() - cooldown_time
                    response = JsonResponse({
                        'error': 'You are in cooldown for favoriting this activity. Please wait {0} to try again.'
                        .format(int(remaining_time.total_seconds() / 60))
                    })
                    response.status_code = 404
                    return response
            added = '#d63031'
            removed = '#b2bec3'
            response = JsonResponse({
                'result': added if created else removed
            })
            response.status_code = 200
            return response
        else:
            response = JsonResponse({
                'error': 'You must login to favorite activities.'
            })
            response.status_code = 404
            return response
