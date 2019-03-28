from django.contrib import admin
from .models import Activity, ActivityReview, Tag, Region

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'host', 'description', 'region', 'featured_photo',
            )
        }),
        ('Activity Information', {
            'classes': ('collapse',),
            'fields': (
                'highlights', 'requirements', 'tags', 'price',
            )
        }),
        ('Location', {
            'classes': ('collapse',),
            'fields': (
                'address', 'latitude', 'longitude'
            )
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': (
                'approved',
            )
        })
    )
    list_display = (
        'title', 'host', 'created', 'review_count',
    )
    readonly_fields = ('slug', 'review_count', 'created',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'created', )
    list_filter = ('created', 'modified', )
    search_fields = ('user', 'content')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Region)
admin.site.register(ActivityReview, ReviewAdmin)
