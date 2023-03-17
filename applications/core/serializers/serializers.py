from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from applications.common.choices import CurrencyChoices
from applications.common.serializers.base import BaseSerializer, BaseModelSerializer
from applications.common.utils.time import get_now
from applications.core.models import Reserve, Amenities


# from applications.common.choices import CurrencyChoices
# from applications.core.models import Room, Place, Reserve, Cost, Amenities
# from applications.user.serializers import OwnerSerializers
#
#
class AmenitiesSerializer(BaseModelSerializer):
    class Meta:
        model = Amenities
        fields = ['name', 'type']


#
#     @staticmethod
#     def get_type_name(obj):
#         return CurrencyChoices.names[obj.type]
#

class ReserveSerializer(BaseModelSerializer):
    class Meta:
        model = Reserve
        exclude = []


class BaseReserveRequestSerializer(BaseSerializer):
    in_datetime = serializers.DateTimeField()
    out_datetime = serializers.DateTimeField()
    people_count = serializers.IntegerField(default=1)

    def validate(self, attrs):
        error = []
        msg = 'Earlier times are not acceptable'
        if not attrs['in_datetime'] >= get_now():
            error.append({"in_date": msg})

        if not attrs['out_datetime'] >= get_now():
            error.append({"out_date": msg})

        if attrs['in_datetime'] >= attrs['out_datetime']:
            error.append({"out_date_and_in_date": 'out_date must greate than in_data'})

        if error:
            raise ValidationError(error)
        return super(BaseReserveRequestSerializer, self).validate(attrs)


class ReserveRequestSerializer(BaseReserveRequestSerializer):
    type = serializers.IntegerField(help_text=f"{CurrencyChoices.choices}", default=0)
    charge = serializers.IntegerField(default=0)


class SearchRequestSerializer(BaseReserveRequestSerializer):
    country = serializers.CharField(allow_null=True)
    city = serializers.CharField(allow_null=True)

    fee_currency = serializers.CharField(allow_null=True)
    fee_min = serializers.IntegerField(allow_null=True)
    fee_max = serializers.IntegerField(allow_null=True)

    room_amenities = serializers.ListSerializer(child=serializers.IntegerField(), help_text="room amenities")
    place_amenities = serializers.ListSerializer(child=serializers.IntegerField(), help_text="place amenities")

    def validate(self, attrs):
        super(SearchRequestSerializer, self).validate(attrs)
        error = []
        if attrs['city'] and not attrs['country']:
            error.append({"country": 'country field needed'})

        if attrs['fee_currency'] or attrs['fee_min'] or attrs['fee_max']:
            if not (attrs['fee_currency'] or attrs['fee_min'] or attrs['fee_max']):
                error.append({"fee": 'some fields missed'})
        if error:
            raise ValidationError(error)
        return super(BaseReserveRequestSerializer, self).validate(attrs)
