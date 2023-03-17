from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from applications.common.models import Configuration, JsonConfig


class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['updated_time', 'created_time', ]
    list_display_fields = []

    def get_readonly_fields(self, request, obj=None):
        all_fields = ['uuid', 'created_time', 'updated_time']
        return all_fields

    def get_list_display(self, request):
        return self.list_display_fields if self.list_display_fields else self.list_display


@admin.register(Configuration)
class ConfigurationAdmin(BaseAdmin):
    pass


@admin.register(JsonConfig)
class JsonConfigAdmin(BaseAdmin):
    pass
