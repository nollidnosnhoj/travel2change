from django.contrib import admin
from .models import PointValue, AwardedPoint

class AwardedPointAdmin(admin.ModelAdmin):
    list_display = ('target', 'key', 'points', 'reason')
    fieldsets = (
        (None, {'fields': ('target', 'points', 'reason', )}),
    )


admin.site.register(PointValue)
admin.site.register(AwardedPoint, AwardedPointAdmin)
