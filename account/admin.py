from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class UserModel(UserAdmin):
    ordering = ('email',)
    list_display = ['username', 'email', 'user_type', 'gender', 'profile_pic', 'other_name', 'address']
    list_filter = ['user_type', 'gender']
    search_fields = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','is_active', 'is_staff', 'is_superuser'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        #form.base_fields['profile_pic'].widget.can_change_related = True
        return form
admin.site.register(CustomUser, UserModel)