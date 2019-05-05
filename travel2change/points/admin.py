from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import PointValue, AwardedPoint

class AwardedPointResources(resources.ModelResource):
    target = fields.Field(
        column_name='target',
        attribute='target',
        widget=ForeignKeyWidget(get_user_model(), 'email'),
    )
    point_value = fields.Field(
        column_name='point_value',
        attribute='point_value',
        widget=ForeignKeyWidget(PointValue, 'key'),
    )
    class Meta:
        model = AwardedPoint
        fields = ('id', 'target', 'point_value', 'points', 'reason', )

class PointValueResources(resources.ModelResource):
    class Meta:
        model = PointValue
        fields = ('id', 'key', 'value', )

class AwardedPointAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AwardedPointResources
    list_display = ('target', 'key', 'points', 'reason')
    fieldsets = (
        (None, {'fields': ('target', 'points', 'reason', )}),
    )

class PointValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PointValueResources
    list_display = ('key', 'value', )


admin.site.register(PointValue, PointValueAdmin)
admin.site.register(AwardedPoint, AwardedPointAdmin)
