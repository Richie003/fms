from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserBio

admin.site.site_header = 'File Manager | Admin'
admin.site.index_title = 'File Manager Admin'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'username', 'full_name', 'ip', 'tel')
    list_filter = ('admin', 'auser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'full_name', 'ip', 'tel')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'auser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'full_name', 'ip', 'tel')}
         ),
    )
    search_fields = ('email', 'username', 'full_name', 'ip', 'tel')
    ordering = ('email', 'username', 'full_name', 'ip', 'tel')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


admin.site.register(UserBio)
