from django.contrib import admin

from applications.common.admin import BaseAdmin

from applications.core.models import *




@admin.register(Place)
class PlaceAdmin(BaseAdmin):
    pass


@admin.register(Amenities)
class AmenitiesAdmin(BaseAdmin):
    pass


@admin.register(Cost)
class CostAdmin(BaseAdmin):
    pass


@admin.register(Room)
class RoomAdmin(BaseAdmin):
    pass


@admin.register(Reserve)
class ReserveAdmin(BaseAdmin):
    pass
