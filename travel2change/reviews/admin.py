from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import ActivityReview

class ActivityReviewInline(admin.TabularInline):
    model = ActivityReview

class ActivityReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'activity', )}),
        (_('Content'), {'fields': ('content', )}),
        (_('Rating'), {'fields': ('rating', )}),
        (_('Photo'), {'fields': ('photo', )}),
        (_('Options'), {'fields': ('show_name', 'show_email', )})
    )
    list_display = ('activity', 'user', 'rating', 'created', )
    list_filter = ('activity', 'created', 'modified', )
    search_fields = ('user', 'activity', )
    readonly_fields = ('created', 'modified', )


admin.site.register(ActivityReview, ActivityReviewAdmin)
