from applications.common.serializers.base import BaseModelSerializer
from applications.core.models import Room
from applications.core.serializers.place_seriaiizers import SearchPlaceSerializer
from applications.core.serializers.serializers import AmenitiesSerializer


class RoomSerializers(BaseModelSerializer):
    class Meta:
        model = Room
        exclude = []


class SearchRoomSerializer(BaseModelSerializer):
    place = SearchPlaceSerializer()
    amenities = AmenitiesSerializer(many=True)

    class Meta:
        model = Room
        exclude = []
