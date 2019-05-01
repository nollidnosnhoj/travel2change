from django.contrib import admin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from activities.models import Activity, ActivityPhoto, Category, Tag, Region

class ActivityPhotosInline(admin.TabularInline):
    model = ActivityPhoto

class ActivityAdmin(FrontendEditableAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Essential Information', {'fields': ('title', 'slug', 'host', 'status', 'is_featured', )}),
        ('Activity Information', {'fields': ('description', 'region', 'categories', 'tags', )}),
        ('Pricing and FareHarbor Item', {'fields': ('price', 'fh_item_id', )}),
        ('Highlights and Requirements', {'fields': ('highlights', 'requirements', )}),
        ('Featured Photo', {'fields': ('featured_photo', )}),
        ('Location', {'fields': ('address', 'latitude', 'longitude', )}),
    )
    list_display = (
        'title', 'host', 'region', 'status', 'created', 'review_count',
    )
    list_filter = (
        'region', 'status',
    )
    readonly_fields = ('slug', 'created',)
    inlines = [ActivityPhotosInline, ]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Region)
