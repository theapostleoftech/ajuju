# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import UserModel


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin class for the UserModel. Enhances the default UserAdmin
    with custom forms and fieldsets.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    # Fields to be used in displaying the User model.
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
