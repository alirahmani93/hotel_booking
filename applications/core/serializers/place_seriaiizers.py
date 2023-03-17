from applications.common.serializers.base import BaseModelSerializer
from applications.core.models import Place
from applications.core.serializers.serializers import AmenitiesSerializer
from applications.user.serializers import OwnerSerializers


class PlaceSerializer(BaseModelSerializer):
    class Meta:
        model = Place
        exclude = []
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class CreatePlaceSerializers(BaseModelSerializer):
    class Meta:
        model = Place
        exclude = ['owner']


class SearchPlaceSerializer(BaseModelSerializer):
    owner = OwnerSerializers(read_only=True)
    amenities = AmenitiesSerializer(many=True)

    class Meta:
        model = Place
        exclude = []
        extra_kwargs = {
            'owner': {'read_only': True}
        }
