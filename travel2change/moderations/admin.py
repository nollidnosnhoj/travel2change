from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from activities.admin import ActivityPhotosInline
from activities.models import Activity

class UnapprovedActivity(Activity):
    class Meta:
        proxy = True
        verbose_name = _('Unapproved Activity')
        verbose_name_plural = _('Unapproved Activities')


class UnapprovedActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Essential Information', {'fields': ('title', 'slug', 'host', 'status', 'is_featured', )}),
        ('Activity Information', {'fields': ('description', 'region', 'categories', 'tags', )}),
        ('Pricing and FareHarbor Item', {'fields': ('price', 'fh_item_id', )}),
        ('Highlights and Requirements', {'fields': ('highlights', 'requirements', )}),
        ('Featured Photo', {'fields': ('featured_photo', )}),
        ('Location', {'fields': ('address', 'latitude', 'longitude', )}),
    )
    list_display = (
        'title', 'host', 'region', 'created',
    )
    readonly_fields = ('slug', 'created',)
    inlines = [ActivityPhotosInline, ]
    def has_add_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        return self.model.objects.unapproved().order_by('-created')


admin.site.register(UnapprovedActivity, UnapprovedActivityAdmin)
