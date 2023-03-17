from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from applications.common.serializers.base import BaseModelSerializer, BaseSerializer
from applications.user.models import Owner, User


class ProfileSerializer(BaseModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["is_verified", "mobile_number", "avatar", "email"]


class OwnerSerializers(BaseModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = ["user", "compony_name"]


class SignupSerializer(BaseModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "mobile_number", "email", "province", "city", "ID_card", "password", "password_repeat"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if not attrs["password"] == attrs["password_repeat"]:
            raise ValidationError("passwords do not match!")
        return super(SignupSerializer, self).validate(attrs)


class ResendSerializer(BaseSerializer):
    email = serializers.EmailField()


class VerifySerializer(ResendSerializer):
    otp = serializers.CharField()


class OwnerSerializer(BaseModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Owner
        exclude = []
