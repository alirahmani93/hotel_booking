from django.contrib import admin

from applications.common.admin import BaseAdmin

from applications.user.models import *


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ['email', ]


@admin.register(Owner)
class OwnerAdmin(BaseAdmin):
    list_display = ['user', 'compony_name']
