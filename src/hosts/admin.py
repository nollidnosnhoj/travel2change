from django.contrib import admin
from .models import Host


class HostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Host Information', {
            'fields': (
                '_name', 'description',
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone', 'website',
            )
        })
    )
    list_display = (
        'user', 'name', 'phone',
    )


admin.site.register(Host, HostAdmin)
