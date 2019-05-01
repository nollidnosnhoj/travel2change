from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Review

class ReviewInline(admin.TabularInline):
    model = Review

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'activity', )}),
        (_('Content'), {'fields': ('content', )}),
        (_('Rating'), {'fields': ('rating', )}),
        (_('Photo'), {'fields': ('photo', )}),
        (_('Options'), {'fields': ('show_name', 'show_email', )})
    )
    list_display = ('activity', 'user', 'rating', 'created', )
    search_fields = ('user', 'activity', )
    readonly_fields = ('created', 'modified', )


admin.site.register(Review, ReviewAdmin)
