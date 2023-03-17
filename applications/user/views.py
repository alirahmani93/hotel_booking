from django.core.cache import cache
from django.db.transaction import atomic
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes as perm
from rest_framework.permissions import AllowAny, IsAuthenticated

from applications.common.statuses import *
from applications.common.utils.email import send_email
from applications.common.utils.response import custom_response
from applications.common.views import BaseViewSet
from applications.user.models import User, Owner
from applications.user.serializers import UserSerializer, SignupSerializer, VerifySerializer, ProfileSerializer, \
    OwnerSerializer, ResendSerializer


class UserViewSet(mixins.ListModelMixin, BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        print(self.queryset.filter(id=self.request.user.id)
              )
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"], url_name="profile", url_path="profile", serializer_class=ProfileSerializer)
    def profile(self, request, *args, **kwargs):
        return custom_response(status_code=OK_200, data=self.serializer_class(self.get_queryset().first()).data)


class AuthViewSet(mixins.ListModelMixin, BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @atomic
    @action(detail=False, methods=["POST"], url_name="email-signup", url_path="email/signup",
            serializer_class=SignupSerializer)
    def signup(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        email = valid_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            return custom_response(
                status_code=USER_ALREADY_EXISTS_461,
                data={}
            )
        new_user = User.objects.create(
            username=valid_data['username'],
            mobile_number=valid_data['mobile_number'],
            email=email,
            province=valid_data['province'],
            city=valid_data['city'],
            ID_card=valid_data['ID_card'],
            is_verified=False,
            is_active=True
        )
        new_user.set_password(valid_data['password'])
        new_user.save()
        send_email(email=email)
        return custom_response(
            status_code=OK_200,
            data=UserSerializer(new_user).data
        )

    @action(detail=False, methods=["POST"], url_name="verify-email", url_path="email/verify",
            serializer_class=VerifySerializer)
    def email_verify(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        email = valid_data['email']
        if not cache.get(email) == valid_data['otp']:
            return custom_response(
                status_code=OTP_EXPIRED,
                data={}
            )

        user = User.objects.filter(email=email)
        if not user.exists():
            return custom_response(
                status_code=USER_NOT_FOUND_450,
                data={}
            )
        user = user.first()
        user.is_verified = True
        user.save()
        return custom_response(
            status_code=OK_200,
            data=UserSerializer(user).data
        )

    @action(detail=False, methods=["POST"], url_name="resend-email", url_path="email/resend",
            serializer_class=ResendSerializer)
    @atomic
    def resend_otp(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        email = valid_data['email']

        user = User.objects.filter(email=email)
        if not user.exists():
            return custom_response(
                status_code=USER_NOT_FOUND_450,
                data={}
            )
        user = user.first()
        user.is_verified = True
        user.save()
        send_email(email=email)

        return custom_response(status_code=OK_200, data={})

    # @TODO:Sign up as owner
    # @TODO:Sign in as owner


class OwnerViewSet(mixins.ListModelMixin, BaseViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["GET"], url_name="profile", url_path="profile", )
    def owner_profile(self, request, *args, **kwargs):
        return custom_response(status_code=OK_200, data=self.serializer_class(self.get_queryset().first()).data)

    # @TODO: request for accept as owner
