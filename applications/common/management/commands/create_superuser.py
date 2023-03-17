import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_superuser()

    @atomic
    def create_superuser(self):
        user = get_user_model()
        u, is_created = user.objects.get_or_create(
            username=os.getenv("ROOT_USER_NAME", default="root"),
            mobile_number=os.getenv("ROOT_USER_MOBILE_NUMBER", default="09000000001"),
            email=os.getenv("ROOT_USER_EMAIL", default="root@test.com"),
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        if not is_created:
            print('root user already created')
        else:
            u.set_password(os.getenv("ROOT_USER_PASSWORD", default="123"))
            u.save()
            print('root user created')
