from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField
from applications.common.utils.time import standard_timestamp_response, standard_date_time_response


class BaseSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseModelSerializer(ModelSerializer):
    # created_time = SerializerMethodField()
    # updated_time = SerializerMethodField()

    # @staticmethod
    # def get_created_time(obj):
    #     if obj.created_time:
    #         return standard_date_time_response(obj.created_time)
    #     return obj.created_time
    #
    # @staticmethod
    # def get_updated_time(obj):
    #     if obj.updated_time:
    #         return standard_date_time_response(obj.updated_time)
    #     return obj.updated_time

    pass
