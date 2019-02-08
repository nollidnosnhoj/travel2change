from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'organization', 
        'is_active', 
        'is_staff', 
        'date_joined'
    )
    list_filter = ('is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Information', {'fields': ('first_name', 'last_name', 'organization',)}),
        ('Permissions', {'fields': ('is_active','is_staff','groups','user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes':('wide'),
            'fields': (
                'email', 
                'first_name', 
                'last_name', 
                'password1', 
                'password2', 
                'groups',
                'user_permissions'
            )
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'organization',)
    ordering = ('email', 'first_name', 'last_name', 'organization', 'date_joined',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
   