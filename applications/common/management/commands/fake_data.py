import os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.transaction import atomic

from applications.common.utils.time import get_now
from applications.core.models import *
from applications.user.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fake_data()

    @atomic
    def fake_data(self):
        user, _ = User.objects.get_or_create(
            email='root@test.com',
            **{"username": 'root@test.com', "ID_card": 'id_id_id', "is_staff": True, "is_superuser": True})
        user.set_password('123')
        user.save()
        passenger, _ = User.objects.get_or_create(username='passenger@test.com', email='passenger@test.com',
                                                  ID_card='passenger')
        owner, _ = Owner.objects.get_or_create(user=user, compony_name='my_compony')
        cost, _ = Cost.objects.get_or_create(type=0, fee_each_day=10)
        amenities_share, _ = Amenities.objects.get_or_create(is_shared=True, name='wifi', type=1)
        amenities_wifi, _ = Amenities.objects.get_or_create(is_shared=False, name='coffee', type=1)
        place_category, _ = PlaceCategory.objects.get_or_create(name="hotel")
        place, _ = Place.objects.get_or_create(
            is_ready=True,
            owner=owner,
            name='SweetHotel',
            geolocation_x=123,
            geolocation_y=321,
            type=place_category,
            area=200,
            rate=3,
            policies='policies text',
            description='description text',
        )
        place.amenities.add(amenities_share)
        place.save()
        room, _ = Room.objects.get_or_create(
            is_ready=True,
            place=place,
            bed_count=5,
            bathroom_count=1,
            area=50,
            description="description",
            type=CurrencyChoices.DOLLAR,
            fee_each_day=10,
            room_number='1'
        )

        reserve, _ = Reserve.objects.get_or_create(
            room=room,
            passenger=passenger,
            people_count=2,
            in_datetime=get_now(),
            out_datetime=get_now() + timedelta(days=1),
        )
        print('fake data done!')
