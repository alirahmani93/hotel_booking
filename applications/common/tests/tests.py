import json

from django.core.cache import cache
from rest_framework.reverse import reverse

from applications.common.models import Configuration, JsonConfig
from applications.common.tests.tests_base import BaseTestCase
from booking import settings


class CommonBaseTestCase(BaseTestCase):
    def setUp(self, empty=False) -> None:
        super(CommonBaseTestCase, self).setUp(empty=empty)
        Configuration.objects.all().delete()
        JsonConfig.objects.all().delete()


class CommonTestCase(CommonBaseTestCase):
    def setUp(self, empty=False) -> None:
        super(CommonTestCase, self).setUp(empty=False)
        cache.clear()
        self.json_config, _ = JsonConfig.objects.get_or_create(name='config', config={"A": "A"})
        self.config, _ = Configuration.objects.get_or_create()
        self.config.config.add(self.json_config)
        self.config.save()

    def test_app_config(self):
        self.response = self.client.get(reverse('app-list'))
        self.assertEqual(
            self.check_response(),
            {
                'app_name': settings.PROJECT_NAME, 'version': settings.VERSION, 'social_media_link': None,
                'deep_link_prefix': '', 'maintenance_mode': False, 'bypass_verification_email': False,
                'server_time_zone': 'Asia/Tehran', 'server_time': self.decoded['server_time'],
                'config': [],
            }
        )

    def test_ping(self):
        self.response = self.client.get(reverse('app-ping'))
        self.assertEqual(self.check_response(), {'detail': 'PONG'})

    def test_health(self):
        self.response = self.client.get(reverse('app-health'))
        self.assertEqual(
            self.check_response(),
            {'app_name': settings.PROJECT_NAME, 'version': settings.VERSION, 'app': True, 'database': True,
             'redis': True})

    def test_time(self):
        self.response = self.client.get(reverse('app-time'))
        self.assertEqual(self.check_response(), {'time': self.decoded['time']})


class JsonConfigTestCase(CommonBaseTestCase):
    """Test suite for the JsonConfig."""

    def setUp(self, empty=False):
        """Define the test client and other test variables."""
        JsonConfig.objects.all().delete()

    def test_duplicated_warning(self):
        """
        Test the create Json Config warning
        """
        new_json, _ = JsonConfig.objects.get_or_create(**{
            "name": "json",
            "is_active": True,
            "config": {
                "A": "AA"
            },
            "min_client_version": 6,
            "max_client_version": 12
        })
        new_json2, _ = JsonConfig.objects.get_or_create(**{
            "name": "json2",
            "is_active": True,
            "config": {
                "A": "AA"
            },
            "min_client_version": 6,
            "max_client_version": 12
        })
        self.assertEqual({'different_values': {}, 'duplicated': {'json2.config.A': 'AA'}},
                         JsonConfig.objects.all().first()._warning())

    def test_different_values_warning(self):
        """
        Test the creation Json Config warning
        """
        self.setUp()
        new_json, _ = JsonConfig.objects.get_or_create(**{
            "name": "json3",
            "is_active": True,
            "config": {
                "A": "B"
            },
            "min_client_version": 6,
            "max_client_version": 12
        })
        self.assertEqual({'different_values': {}, 'duplicated': {}}, JsonConfig.objects.all().last()._warning())
