import abc

from django.db import connections

from django_redis import get_redis_connection
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.common.models import Configuration
from applications.common.serializers.serializers import HealthSerializer, ConfigurationSerializers
from applications.common.utils.email import logging
from applications.common.utils.time import get_now, standard_response_datetime
from booking.settings import PROJECT_NAME, VERSION


class BaseViewSet(viewsets.GenericViewSet, abc.ABC):
    serializer_classes: dict = {}

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def data_validation(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer, serializer.validated_data

    def get_serializer_class(self):
        version = '' if self.request.version is None else self.request.version
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action][version] if version in self.serializer_classes[self.action] \
                else self.serializer_classes[self.action][list(self.serializer_classes[self.action].keys())[-1]]
        return self.serializer_class


class BaseAPIView(APIView, abc.ABC):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def data_validation(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer, serializer.validated_data


class AppViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ConfigurationSerializers

    def list(self, request, *args, **kwargs):
        """Return data what Non-sensitive information. """
        data: dict = Configuration.load()
        result = self.serializer_class(data).data
        result['server_time'] = standard_response_datetime(get_now())
        return Response(data=result)

    @action(methods=['GET'], detail=False, url_path='time', url_name='time')
    def time(self, request, *args, **kwargs):
        return Response(data={'time': standard_response_datetime(get_now())})

    @action(methods=['GET'], detail=False, url_path='ping', url_name='ping', permission_classes=(IsAuthenticated,))
    def ping(self, request, *args, **kwargs):
        return Response(data={'detail': 'PONG'})

    @action(methods=['GET'], detail=False, url_path='health', url_name='health', serializer_class=HealthSerializer)
    def health(self, request, *args, **kwargs):

        def app():
            app = 1
            return app

        def database():
            # Postgres
            postgres = 0
            try:
                db_conn = connections['default']
                db_conn.cursor()
                postgres = 1
            except:
                logging.error(msg={"postgres": "Postgres Server not available"})
                print(">>>", "Postgres not available")

            if postgres:
                return 1
            else:
                return 0

        def redis():
            status = 0

            try:
                redis_check = get_redis_connection()
                if redis_check:
                    status = 1
                    return status
                return status
            except:
                logging.error(msg={"redis": "redis Server not available"})
                print(">>>", "redis Server not available")

                return status

        return Response(HealthSerializer({
            "app_name": PROJECT_NAME,
            'version': VERSION,
            'app': app(),
            'database': database(),
            'redis': redis(),
        }).data)
