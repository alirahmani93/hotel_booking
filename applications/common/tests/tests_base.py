import json

from django.test import TestCase
from requests import Response

from applications.common.models import JsonConfig, Configuration
from applications.user.models import User


class BaseTestCase(TestCase):

    def setUp(self, empty=False) -> None:
        super(BaseTestCase, self).setUp()

        self.user_email = 'ali93rahmani@gmail.com'
        self.user_password = 'ali93rahmani@gmail.com'
        self.json_config, _ = JsonConfig.objects.get_or_create(name='config', config={"A": "A"})
        self.config, _ = Configuration.objects.get_or_create()

        self.user, _ = User.objects.get_or_create(username=self.user_email, email=self.user_email)
        self.user.set_password(self.user_password)
        self.user.save()

        self.client.login(username=self.user_email, email=self.user_email, password=self.user_password)
        self.response = None
        self.decoded: dict = {}

    def check_status_code(self, status_code: int = 200):
        self.assertEqual(self.response.status_code, status_code)

    def check_response(self, status_code: int = 200):
        self.check_status_code(status_code=status_code)
        self.decoded = json.loads(self.response.content.decode())
        return self.decoded

    def clean(self):
        self.decoded = {}
        self.response = None

    def tearDown(self) -> None:
        super().tearDown()
        self.clean()
