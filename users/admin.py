from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group as DjangoGroup
from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import AppUser, AppGroup


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)


class AppUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("middle_name", 'is_active', 'is_superuser')
    add_form = UserCreationFormExtended
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'is_active')
        }),
    )


admin.site.unregister(DjangoGroup)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(AppGroup, GroupAdmin)
