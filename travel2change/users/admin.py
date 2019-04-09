from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import Host

User = get_user_model()


class HostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Host Information', {
            'fields': (
                '_name', 'description',
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone', 'website',
            )
        })
    )
    list_display = (
        'user', 'name', 'phone',
    )


class HostAdminInline(admin.TabularInline):
    model = Host


class CustomUserAdmin(UserAdmin):
    inlines = [HostAdminInline, ]
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined'
    )
    list_filter = ('is_active', 'is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email', 'first_name', 'last_name', 'date_joined',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Host, HostAdmin)
