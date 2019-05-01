from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from points.models import points_awarded
from users.models import Host

User = get_user_model()


class HostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Information', {'fields': ('_name', 'description', 'fh_username',)}),
        ('Contact Information', {'fields': ('phone', 'website',)})
    )
    list_display = (
        'user', 'name', 'phone',
    )


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined',
        'points',
    )
    list_filter = ('is_active', 'is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        }),
        ('Permissions', {
            'classes': ('wide', ),
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            )
        })
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email', 'first_name', 'last_name', 'date_joined',)
    filter_horizontal = ()

    # get points for the user
    def points(self, obj):
        return points_awarded(obj)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Host, HostAdmin)
