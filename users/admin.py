from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from users.models import AppUser, AppGroup

admin.site.unregister(Group)
admin.site.register(AppUser, UserAdmin)
admin.site.register(AppGroup, GroupAdmin)
