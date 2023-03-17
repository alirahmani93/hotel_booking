from rest_framework.fields import BooleanField, CharField
from rest_framework.serializers import ModelSerializer

from applications.common.models import Configuration, JsonConfig
from applications.common.serializers.base import BaseSerializer


class HealthSerializer(BaseSerializer):
    app_name = CharField(max_length=256)
    version = CharField(max_length=100)
    app = BooleanField()
    database = BooleanField()
    redis = BooleanField()


class JsonConfigModelSerializers(ModelSerializer):
    class Meta:
        model = JsonConfig
        exclude = ['updated_time', 'created_time', 'uuid', 'id', 'is_active', ]


class ConfigurationSerializers(ModelSerializer):
    config = JsonConfigModelSerializers(many=True)

    class Meta:
        model = Configuration
        fields = [
            'app_name',
            'version',
            'social_media_link',
            'config',
            'deep_link_prefix',
            'maintenance_mode',
            'bypass_verification_email',
            'server_time_zone',
            'server_time',
        ]
