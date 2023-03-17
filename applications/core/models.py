from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _

from applications.common.choices import CurrencyChoices, AmenitiesChoices
from applications.common.models import BaseModel, Address
from applications.common.utils.handler import get_name_from_integer_choices
from applications.user.models import User, Owner


class Cost(BaseModel):
    type = models.IntegerField(verbose_name=_('type'), choices=CurrencyChoices.choices, default=CurrencyChoices.DOLLAR)
    fee_each_day = models.FloatField(verbose_name=_('fee_each_day'), default=0)

    def __str__(self):
        return f"{self.fee_each_day} ({get_name_from_integer_choices(CurrencyChoices, self.type)}))"


class Amenities(BaseModel):
    is_shared = models.BooleanField(verbose_name=_('is_shared'), default=False,
                                    help_text="all room have these amenities or not?")
    name = models.CharField(verbose_name=_('name'), max_length=255)
    type = models.PositiveIntegerField(verbose_name=_('type'), choices=AmenitiesChoices.choices)

    def __str__(self):
        return f"{self.name} ({get_name_from_integer_choices(AmenitiesChoices, self.type)})"


class PlaceCategory(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)

    def __str__(self):
        return self.name


class BaseDetail(BaseModel):
    is_ready = models.BooleanField(verbose_name=_('is_ready'), default=False)
    area = models.PositiveIntegerField(verbose_name=_('area'), help_text='square meter')
    description = models.TextField(verbose_name=_('description'), max_length=5000)
    amenities = models.ManyToManyField(verbose_name=_('amenities'), to=Amenities)

    class Meta:
        abstract = True


class Place(BaseDetail, Address):
    owner = models.ForeignKey(verbose_name=_('owner'), to=Owner, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('name'), max_length=255)

    type = models.ForeignKey(verbose_name=_('type'), to=PlaceCategory, on_delete=models.CASCADE)

    rate = models.PositiveIntegerField(verbose_name=_('rate'), default=0)

    policies = models.TextField(verbose_name=_('policies'), )
    amenities = models.ManyToManyField(verbose_name=_('amenities'), to=Amenities, limit_choices_to={"is_shared": True})

    discount_for_full_rent = models.PositiveSmallIntegerField(verbose_name=_('discount_for_full_rent'), default=0,
                                                              help_text='percentage',
                                                              validators=[MaxValueValidator(100)])

    list_display_fields = ['owner', 'type', 'is_ready', 'area', ]

    def __str__(self):
        return f'{self.type}({self.owner})'

    class Meta:
        unique_together = ['owner', 'name']

    @staticmethod
    def prepare_data_to_create(owner: Owner, valid_data: dict) -> dict:
        return {
            'owner': owner,
            'name': valid_data['name'],
            'type': valid_data['type'],
            'rate': valid_data['rate'],
            'policies': valid_data['policies'],
            'discount_for_full_rent': valid_data['discount_for_full_rent'],
            'is_ready': valid_data['is_ready'],
            'area': valid_data['area'],
            'description': valid_data['description'],
            'geolocation_x': valid_data['geolocation_x'],
            'geolocation_y': valid_data['geolocation_y'],
            'country': valid_data['country'],
            'city': valid_data['city'],
            'main_street': valid_data['main_street'],
            'street': valid_data['street'],
            'house_number': valid_data['house_number'],
            'floor': valid_data['floor'],
            'extra_address_detail': valid_data['extra_address_detail'],
            'zipcode': valid_data['zipcode'],
        }


class Room(BaseDetail):
    place = models.ForeignKey(verbose_name=_('place'), to=Place, on_delete=models.CASCADE)
    room_number = models.CharField(verbose_name=_('room_number'), max_length=255)

    bed_count = models.PositiveIntegerField(verbose_name=_('bed_count'), )
    bathroom_count = models.PositiveIntegerField(verbose_name=_('bathroom_count'), )

    amenities = models.ManyToManyField(verbose_name=_('amenities'), to=Amenities, limit_choices_to={"is_shared": False})

    type = models.IntegerField(verbose_name=_('type'), choices=CurrencyChoices.choices, default=CurrencyChoices.DOLLAR)
    fee_each_day = models.FloatField(verbose_name=_('fee_each_day'), default=0)

    list_display_fields = ['place', 'room_number', 'bed_count', 'bathroom_count', 'is_ready', 'area', 'type',
                           'fee_each_day', ]

    def __str__(self):
        return f'{self.place}({self.bed_count})'

    @classmethod
    def activated_room(cls):
        return cls.objects.filter(is_active=True, is_ready=True)

    class Meta:
        unique_together = ['place', 'room_number']

    @staticmethod
    def prepare_room_data_for_create(valid_data: dict) -> dict:
        return {
            "is_ready": valid_data['is_ready'],
            "area": valid_data['area'],
            "description": valid_data['description'],
            "room_number": valid_data['room_number'],
            "bed_count": valid_data['bed_count'],
            "bathroom_count": valid_data['bathroom_count'],
            "type": valid_data['type'],
            "fee_each_day": valid_data['fee_each_day'],
            "place": valid_data['place'],
        }


class Reserve(BaseModel):
    room = models.ForeignKey(verbose_name=_('room'), to=Room, on_delete=models.PROTECT)
    passenger = models.ForeignKey(verbose_name=_('passenger'), to=User, on_delete=models.PROTECT)

    people_count = models.PositiveIntegerField(verbose_name=_('people_count'), default=1)
    in_datetime = models.DateTimeField(verbose_name=_('in date time'), )
    out_datetime = models.DateTimeField(verbose_name=_('out date time'), )

    is_canceled = models.BooleanField(verbose_name=_('is_canceled'), default=False)
    is_extended = models.BooleanField(verbose_name=_('is_extended'), default=False)
    is_damaged = models.BooleanField(verbose_name=_('is_damaged'), default=False)

    type = models.IntegerField(verbose_name=_('type'), choices=CurrencyChoices.choices, default=CurrencyChoices.DOLLAR)
    charge = models.FloatField(verbose_name=_('charge'), default=0)

    list_display_fields = ['place', 'bed_count', 'bathroom_count', 'is_ready', 'area', 'fee']

    @classmethod
    def reserve_exclude_options(cls, valid_data):
        return cls.objects.select_related("room").filter(
            in_datetime__gte=valid_data["in_datetime"], out_datetime__lte=valid_data["out_datetime"],
            room__bed_count__lte=valid_data["people_count"]
        )
