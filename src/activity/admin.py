from django.contrib import admin
from .models import (Activity, Tag, Region)

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title', 'host', 'description', 'region',
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
        })
    )
    list_display = (
        'title', 'host', 'created', 'review_count',
    )
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('review_count', 'created',)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Region)
