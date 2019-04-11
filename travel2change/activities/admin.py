from django.contrib import admin
from activities.models import Activity, ActivityPhoto, Category, Tag, Region

class ActivityPhotosInline(admin.TabularInline):
    model = ActivityPhoto

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'host', 'description', 'region', 'featured_photo',)}),
        ('Information', {'fields': ('highlights', 'requirements', 'categories', 'tags', 'price',)}),
        ('Location', {'fields': ('address', 'latitude', 'longitude')}),
        ('FareHarbor Item', {'fields': ('fh_item_id', )}),
        ('Status', {'fields': ('status', 'is_featured',)}),
    )
    list_display = (
        'title', 'host', 'approved_time', 'review_count',
    )
    readonly_fields = ('slug', 'review_count', 'approved_time',)
    inlines = [ActivityPhotosInline, ]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Region)
