from django.contrib import admin
from activities.models import Activity, ActivityReview, ActivityPhoto, Category, Tag, Region

class ActivityPhotosInline(admin.TabularInline):
    model = ActivityPhoto

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'host', 'description', 'region', 'featured_photo',
            )
        }),
        ('Activity Information', {
            'fields': (
                'highlights', 'requirements', 'categories', 'tags', 'price',
            )
        }),
        ('Location', {
            'fields': (
                'address', 'latitude', 'longitude'
            )
        }),
        ('Status', {
            'fields': (
                'status',
            )
        })
    )
    list_display = (
        'title', 'host', 'approved_time', 'review_count',
    )
    readonly_fields = ('slug', 'review_count', 'approved_time',)
    inlines = [ActivityPhotosInline, ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'created', )
    list_filter = ('created', 'modified', )
    search_fields = ('user', 'content')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(ActivityReview, ReviewAdmin)
