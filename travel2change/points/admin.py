from django.contrib import admin
from .models import PointValue, AwardedPoints

class AwardedPointsAdmin(admin.ModelAdmin):
    list_display = ('target', 'points', 'reason')


admin.site.register(PointValue)
admin.site.register(AwardedPoints, AwardedPointsAdmin)