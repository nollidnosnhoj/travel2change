from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined'
    )
    list_filter = ('is_active', 'is_staff',)
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
