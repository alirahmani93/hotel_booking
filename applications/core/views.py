import datetime

from django.db.models import Sum, Count
from django.db.transaction import atomic
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes as perm

from applications.common.permissions import IsOwner
from applications.common.serializers.base import BaseSerializer
from applications.common.statuses import *
from applications.common.utils.response import custom_response
from applications.common.utils.time import get_now
from applications.common.views import BaseViewSet, BaseAPIView
from applications.core.models import Room, Reserve, Place
from applications.core.serializers.serializers import ReserveSerializer, SearchRequestSerializer, \
    ReserveRequestSerializer
from applications.core.serializers.place_seriaiizers import PlaceSerializer, CreatePlaceSerializers
from applications.core.serializers.room_serializers import RoomSerializers, SearchRoomSerializer
from applications.user.models import User


class PlaceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   BaseViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.filter(is_active=True, is_ready=True)
    permission_classes = [IsOwner | IsAdminUser]

    def list(self, request, *args, **kwargs):
        return custom_response(
            status_code=OK_200,
            data=super().list(request, *args, **kwargs).data,
        )

    @action(detail=False, methods=["GET"], url_name="owner/list", url_path="owner-list",
            serializer_class=CreatePlaceSerializers)
    def list_owner_places(self, request, *args, **kwargs):
        owner = self.request.user.owner
        if not owner:
            return custom_response(status_code=USER_NOT_OWNER_458, data={})

        query = Place.objects.filter(owner=owner)
        return custom_response(
            status_code=OK_200,
            data=self.serializer_class(query, many=True).data,
        )

    @atomic
    def create(self, request, *args, **kwargs):
        if not self.request.user.owner:
            return custom_response(
                status_code=USER_NOT_OWNER_458,
                data={},
            )
        serializer, valid_data = self.data_validation()
        place = Place.objects.filter(owner=self.request.user.owner, name=valid_data['name'])
        if place.exists():
            return custom_response(
                status_code=PLACE_ALREADY_EXISTS_459,
                data=self.serializer_class(place.first()).data,
            )
        new_place = Place.objects.create(
            **Place.prepare_data_to_create(owner=self.request.user.owner, valid_data=valid_data)
        )

        new_place.amenities.add(*[i.id for i in valid_data['amenities']])
        new_place.save()
        return custom_response(
            status_code=CREATED_201,
            data=self.serializer_class(new_place).data,
        )

    @action(detail=True, methods=["POST"], url_name="place/delete", url_path="delete",
            serializer_class=CreatePlaceSerializers)
    @atomic
    def delete_place(self, request, *args, **kwargs):
        place = self.get_object()
        owner = self.request.user.owner
        if place.owner != owner:
            return custom_response(
                status_code=BAD_REQUEST_400,
                data={},
            )
        reserved_rooms = Reserve.objects.filter(room__place=place)
        if reserved_rooms.exists():
            return custom_response(
                status_code=ROOM_ALREADY_RESERVED_454,
                data=ReserveSerializer(reserved_rooms, many=True).data,
            )

        place.delete()
        return custom_response(
            status_code=DELETED_204,
            data={},
        )

    @action(detail=True, methods=["GET"], url_name="capacity", url_path="capacity")
    def capacity(self, request, *args, **kwargs):
        owner = self.request.user.owner
        place = self.get_object()
        if not place.owner == self.request.user.owner:
            return custom_response(
                status_code=OWNERSHIP_ERROR_463,
                data={}
            )

        rooms = Room.objects.filter(place__owner=owner).select_related('place')
        reserved = Reserve.objects.filter(room__in=rooms.values_list('id', flat=True), in_datetime__gt=get_now(),
                                          out_datetime__lte=get_now() + datetime.timedelta(days=1))

        return custom_response(
            status_code=OK_200,
            data={'capacity': rooms.count() - reserved.count()}
        )


class RoomViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, BaseViewSet):
    serializer_class = RoomSerializers
    queryset = Room.objects.filter(is_active=True, is_ready=True)
    permission_classes = [IsOwner | IsAdminUser]

    def list(self, request, *args, **kwargs):
        query = Room.objects.filter(place__owner=self.request.user.owner)
        return custom_response(
            status_code=OK_200,
            data=self.serializer_class(query, many=True).data,
        )

    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        if room.place.owner != self.request.user.owner:
            return custom_response(
                status_code=BAD_REQUEST_400,
                data={}
            )

        return custom_response(
            status_code=OK_200,
            data=self.serializer_class(room).data,
        )

    @atomic
    def create(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        place = Place.objects.filter(id=valid_data['place'].id, owner=self.request.user.owner)
        if not place.exists():
            custom_response(
                status_code=PLACE_NOT_FOUND_457,
                data={},
            )

        room = Room.objects.filter(place=valid_data['place'], room_number=valid_data['room_number'],
                                   place__owner=self.request.user.owner)
        if room.exists():
            custom_response(
                status_code=ROOM_ALREADY_EXISTS_456,
                data={},
            )
        new_room = Room.objects.create(**Room.prepare_room_data_for_create(valid_data=valid_data))
        new_room.amenities.add(*[i.id for i in valid_data['amenities']])
        new_room.save()
        return custom_response(
            status_code=CREATED_201,
            data=self.serializer_class(new_room).data,
        )

    @atomic
    def update(self, request, *args, **kwargs):
        room = self.get_object()
        if room.place.owner != self.request.user.owner:
            return custom_response(
                status_code=BAD_REQUEST_400,
                data={},
            )

        return custom_response(
            status_code=OK_200,
            data=super().update(request, *args, **kwargs).data,
        )

    @action(detail=True, methods=["POST"], url_name="room-delete", url_path="delete",
            serializer_class=CreatePlaceSerializers)
    @atomic
    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        if room.place.owner != self.request.user.owner:
            return custom_response(
                status_code=BAD_REQUEST_400,
                data={},
            )
        reserved_rooms = room.reserve_set.filter(is_active=True)
        if reserved_rooms.exists():
            return custom_response(
                status_code=ROOM_ALREADY_RESERVED_454,
                data=ReserveSerializer(reserved_rooms, many=True).data,
            )
        return custom_response(
            status_code=OK_200,
            data=super().destroy(request, *args, **kwargs).data,
        )

    @perm([IsAuthenticated])
    @atomic
    @action(detail=True, methods=["POST"], url_name="reserve", url_path="reserve",
            serializer_class=ReserveRequestSerializer)
    def reserve(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()

        room = self.get_object()
        reserved = Reserve.objects.filter(
            room=room,
            in_datetime__gte=valid_data["in_datetime"], out_datetime__lte=valid_data["out_datetime"],
            room__bed_count__gte=valid_data["people_count"])
        if reserved.exists():
            return custom_response(
                status_code=ROOM_ALREADY_RESERVED_454,
                data={}
            )

        if room.bed_count < valid_data["people_count"]:
            return custom_response(
                status_code=RESERVE_NOT_ENOUGH_BED_460,
                data={}
            )
        reserve_room = Reserve.objects.create(
            room=room,
            passenger=self.request.user,
            people_count=valid_data["people_count"],
            in_datetime=valid_data["in_datetime"],

            out_datetime=valid_data["out_datetime"],
            type=valid_data["type"],
            charge=valid_data["charge"],
        )

        return custom_response(
            status_code=CREATED_201,
            data=ReserveSerializer(reserve_room).data
        )


class ReserveViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, BaseViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.filter(is_active=True)

    def get_queryset(self):
        return self.queryset.filter(passenger=self.request.user)

    def list(self, request, *args, **kwargs):
        return custom_response(
            status_code=OK_200,
            data=super(ReserveViewSet, self).list(request, *args, **kwargs).data
        )

    def update(self, request, *args, **kwargs):
        return custom_response(
            status_code=OK_200,
            data=super(ReserveViewSet, self).update(request, *args, **kwargs).data
        )

    @perm([IsOwner])
    @action(detail=False, methods=["GET"], url_name="owner", url_path="owner", )
    def list_owner_reserved_room(self, request, *args, **kwargs):
        return custom_response(
            status_code=OK_200,
            data=self.serializer_class(
                Reserve.objects.filter(room__place__owner_id=self.request.user.owner.id).order_by(
                    'room__place'),
                many=True
            ).data
        )


class SearchAPIView(BaseAPIView):
    serializer_class = SearchRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        reserved_ids = Reserve.reserve_exclude_options(valid_data=valid_data).values_list("room", flat=True)

        rooms = Room.activated_room().select_related("place").select_related(
            "place__owner").prefetch_related('amenities').prefetch_related('place__amenities').prefetch_related(
            "reserve_set").exclude(id__in=reserved_ids)
        if valid_data['room_amenities']:
            rooms = rooms.filter(amenities__in=valid_data['room_amenities'])
        if valid_data['place_amenities']:
            rooms = rooms.filter(place__amenities__in=valid_data['place_amenities'])

        if valid_data['country']:
            rooms = rooms.filter(place__country=valid_data['country'])
            if valid_data["city"]:
                rooms = rooms.filter(place__country=valid_data["city"])

        if valid_data['fee_currency']:
            rooms = rooms.filter(type=valid_data['fee_currency'], fee_each_day__gte=valid_data['fee_min'],
                                 fee_each_day__lte=valid_data['fee_max'])

        return custom_response(
            status_code=OK_200,
            data=SearchRoomSerializer(rooms, many=True).data
        )
