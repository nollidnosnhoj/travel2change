from django.contrib import admin
from activities.models import Activity, Tag, Region

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'host', 'description', 'region', 'featured_photo',
            )
        }),
        ('Activity Information', {
            'fields': (
                'highlights', 'requirements', 'tags', 'price',
            )
        }),
        ('Location', {
            'fields': (
                'address', 'latitude', 'longitude'
            )
        }),
        ('Status', {
            'fields': (
                'approved',
            )
        })
    )
    list_display = (
        'title', 'host', 'created', 'review_count',
    )
    readonly_fields = ('slug', 'review_count', 'created',)


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Region)
