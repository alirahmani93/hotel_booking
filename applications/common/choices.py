from django.db import models
from django.utils.translation import gettext_lazy as _


class PlaceChoices(models.IntegerChoices):
    APARTMENT = 1, _("Apartment")
    HOSTEL = 2, _("Hostel")
    HOTEL = 3, _("Hotel")
    ROOM = 4, _("Room")


class CurrencyChoices(models.IntegerChoices):
    DOLLAR = 0, _("Dollar")
    EURO = 1, _("Euro")
    POUND = 2, _("Pound")
    RIAL = 3, _("Rial")


class AmenitiesChoices(models.IntegerChoices):
    FEATURES = 1, _("Features")
    APPLIANCE = 2, _("Appliances")
    OTHER = 3, _("Others")
