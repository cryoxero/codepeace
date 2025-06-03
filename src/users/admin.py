from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'level', 'email', 'is_staff', 'is_active')
    list_filter = ('level', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions'
            ),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)