from django.contrib import admin
from .models import PointValue, AwardedPoint

class AwardedPointAdmin(admin.ModelAdmin):
    list_display = ('target', 'key', 'points', 'reason')

    def key(self, obj):
        return obj.point_value.key


admin.site.register(PointValue)
admin.site.register(AwardedPoint, AwardedPointAdmin)
