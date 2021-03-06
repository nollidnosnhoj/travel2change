from django.contrib import admin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from activities.models import Activity, ActivityPhoto, Category, Tag, Region
from users.models import Host

class ActivityPhotosInline(admin.TabularInline):
    model = ActivityPhoto

class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', )

class TagResources(resources.ModelResource):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', )

class RegionResources(resources.ModelResource):
    class Meta:
        model = Region
        fields = ('id', 'name', 'slug', )
    
class ActivityResources(resources.ModelResource):
    host = fields.Field(
        column_name='host',
        attribute='host',
        widget=ForeignKeyWidget(Host),
    )
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'slug'),
    )
    tags = fields.Field(
        column_name='tags',
        attribute='tags',
        widget=ManyToManyWidget(Tag, ' ', 'slug'),
    )
    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget(Category, ' ', 'slug')
    )
    class Meta:
        model = Activity
        fields = (
            'id',
            'title',
            'host',
            'description',
            'highlights',
            'requirements',
            'region',
            'tags',
            'categories',
            'address',
            'latitude',
            'longitude',
            'price',
            'fh_item_id',
            'status',
        )

class ActivityAdmin(
    FrontendEditableAdminMixin,
        ImportExportModelAdmin,
        ImportExportActionModelAdmin,
        admin.ModelAdmin):
    resource_class = ActivityResources
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

class CategoryAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = CategoryResources
    list_display = ('name', 'slug', )

class TagAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TagResources
    list_display = ('name', 'slug', )

class RegionAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = RegionResources
    list_display = ('name', 'slug', )


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
