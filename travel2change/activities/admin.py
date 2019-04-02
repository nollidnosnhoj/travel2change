from django.contrib import admin
from activities.models import Activity, Category, Tag, Region

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
                'highlights', 'requirements', 'categories', 'tags', 'price',
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
                'status',
            )
        })
    )
    list_display = (
        'title', 'host', 'approved_time', 'review_count',
    )
    readonly_fields = ('slug', 'review_count', 'approved_time',)


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Region)
