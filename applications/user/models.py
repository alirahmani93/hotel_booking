import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.common.fields import MyImageField, MobileNumber
from applications.common.models import BaseModel
from booking import settings


# Create your models here.

class User(BaseModel, AbstractUser):
    def upload_to():
        return f'{settings.MEDIA_ROOT}/user/'

    def default_profile_pic():
        return f"/default_user_profile.png"

    is_verified = models.BooleanField(verbose_name=_('is verified'), default=False)
    mobile_number = MobileNumber(null=True, blank=True)
    avatar = MyImageField(upload_to=upload_to, default=default_profile_pic)
    email = models.EmailField(verbose_name=_('email'), unique=True)

    province = models.CharField(verbose_name=_('province'), max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name=_('city'), max_length=255, null=True, blank=True)
    ID_card = models.CharField(verbose_name=_('ID card'), max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def full_name(self):
        """Creates the users full name"""
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else self.username

    def delete(self, using=None, keep_parents=False):
        """system_user and root can't delete"""
        if self.username in [os.environ.get('SYSTEM_USER_NAME'), os.environ.get('ROOT_USER_NAME')]:
            return  # @TODO: raise or return
        super(User, self).delete(using=None, keep_parents=False)


class Owner(BaseModel):
    is_verified_owner = models.BooleanField(verbose_name=_('is verified owner'), default=False)
    user = models.OneToOneField(verbose_name=_('user'), to=User, on_delete=models.CASCADE, )
    compony_name = models.CharField(verbose_name=_('compony name'), max_length=255, )

    def __str__(self):
        return f"{self.user.email}( {self.compony_name} )"
