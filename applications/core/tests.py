from django.test import TestCase
from rest_framework.reverse import reverse

from applications.common.tests.tests_base import BaseTestCase

from applications.core.models import *


# @TODO: tests needed


class BaseCoreTestCase(BaseTestCase):
    def setUp(self, empty=False) -> None:
        super(BaseCoreTestCase, self).setUp(empty=empty)
        self.amenities_share, _ = Amenities.objects.get_or_create(is_shared=True, name='wifi', type=1)
        self.amenities_wifi, _ = Amenities.objects.get_or_create(is_shared=False, name='coffee', type=1)
        self.place_category, _ = PlaceCategory.objects.get_or_create(name="hotel")


class PlaceTestCase(BaseCoreTestCase):
    def setUp(self, empty=False) -> None:
        super(PlaceTestCase, self).setUp(empty)

    def test_create_place(self):
        data = {
            "name": "SweetHotel5",
            "geolocation_x": 123.0,
            "geolocation_y": 321.0,
            "country": "Iran",
            "city": "a",
            "main_street": "aa",
            "street": "",
            "house_number": "123",
            "floor": "",
            "extra_address_detail": "",
            "zipcode": "",
            "is_ready": True,
            "area": 200,
            "description": "description text",
            "rate": 3,
            "policies": "policies text",
            "discount_for_full_rent": 0,
            "type": 1,
            "amenities": [
                self.amenities_share.id
            ]
        }
        self.response = self.client.post(reverse("place-list"), data=data)
        self.assertEqual(self.check_response(status_code=403),
                         {'detail': 'You do not have permission to perform this action.'})

        Owner.objects.create(user=self.user, compony_name="test_compony")
        self.response = self.client.post(reverse("place-list"), data=data)
        decoded_response = self.check_response(status_code=201)
        self.assertEquals(
            decoded_response,
            {
                "detail": "Created",
                "code": "created",
                "data": {
                    "id": decoded_response['data']['id'],
                    "uuid": decoded_response['data']['uuid'],
                    "is_active": True,
                    "updated_time": decoded_response['data']['updated_time'],
                    "created_time": decoded_response['data']['created_time'],
                    "geolocation_x": 123.0,
                    "geolocation_y": 321.0,
                    "country": "Iran",
                    "city": "a",
                    "main_street": "aa",
                    "street": "",
                    "house_number": "123",
                    "floor": "",
                    "extra_address_detail": "",
                    "zipcode": "",
                    "is_ready": True,
                    "area": 200,
                    "description": "description text",
                    "name": "SweetHotel5",
                    "rate": 3,
                    "policies": "policies text",
                    "discount_for_full_rent": 0,
                    "owner": 1,
                    "type": 1,
                    "amenities": [
                        1
                    ]
                }
            }
        )

        self.response = self.client.post(reverse("place-list"), data=data)
        decoded_response = self.check_response(status_code=459)
        self.assertEquals(decoded_response, {
            "detail": "Place already exists",
            "code": "place_already_exists",
            "data": {
                "id": decoded_response['data']['id'],
                "uuid": decoded_response['data']['uuid'],
                "is_active": True,
                "updated_time": decoded_response['data']['updated_time'],
                "created_time": decoded_response['data']['created_time'],
                "geolocation_x": 123.0,
                "geolocation_y": 321.0,
                "country": "Iran",
                "city": "a",
                "main_street": "aa",
                "street": "",
                "house_number": "123",
                "floor": "",
                "extra_address_detail": "",
                "zipcode": "",
                "is_ready": True,
                "area": 200,
                "description": "description text",
                "name": "SweetHotel5",
                "rate": 3,
                "policies": "policies text",
                "discount_for_full_rent": 0,
                "owner": 1,
                "type": 1,
                "amenities": [
                    1
                ]
            }
        })
