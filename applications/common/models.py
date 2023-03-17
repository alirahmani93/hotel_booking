import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models

from applications.common.fields import MyImageField
from applications.common.utils.time import standard_response_datetime, get_now
from booking import settings


def get_version():
    return settings.VERSION


def get_app_name():
    return settings.PROJECT_NAME


class BaseModel(models.Model):
    uuid = models.UUIDField(verbose_name=_('uuid'), default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    updated_time = models.DateTimeField(verbose_name=_('updated_time'), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_('created_time'), auto_now_add=True)

    list_display_fields = ['uuid', 'is_active', 'updated_time', 'created_time', ]

    class Meta:
        abstract = True


class Address(models.Model):
    geolocation_x = models.FloatField(verbose_name=_('geolocation x'))
    geolocation_y = models.FloatField(verbose_name=_('geolocation y'))
    country = models.CharField(verbose_name=_('country'), max_length=255, default='Iran')
    city = models.CharField(verbose_name=_('city'), max_length=255)
    main_street = models.CharField(verbose_name=_('main_street'), max_length=255)
    street = models.CharField(verbose_name=_('street'), max_length=255, blank=True, null=True)
    house_number = models.CharField(verbose_name=_('house_number'), max_length=255)
    floor = models.CharField(verbose_name=_('floor'), max_length=255, blank=True, null=True)
    extra_address_detail = models.CharField(verbose_name=_('address_extra'), max_length=255, blank=True, null=True)

    zipcode = models.CharField(verbose_name=_("zipcode"), max_length=31, blank=True, null=True)

    class Meta:
        abstract = True


class ImageModel(BaseModel):
    image = MyImageField()

    class Meta:
        abstract = True


class JsonConfig(BaseModel):
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=255)
    config = models.JSONField(verbose_name=_("Config"))
    min_client_version = models.PositiveIntegerField(verbose_name=_("Minimum client version"), default=0)
    max_client_version = models.PositiveIntegerField(verbose_name=_("Maximum client version"), default=1)

    def __check_version_range(self) -> bool:
        return self.min_client_version > self.max_client_version

    def _warning(self) -> dict:
        query = JsonConfig.objects.exclude(uuid=self.uuid)
        different_values, duplicated = {}, {}
        for x in query:
            for i, j in x.config.items():
                if i in self.config.keys():
                    if j == self.config[i]:
                        duplicated[f"{x.name}.config.{i}"] = self.config[i]
                    else:
                        different_values[f"{x.name}.config.{i}"] = self.config[i]
        return {"different_values": different_values, "duplicated": duplicated}

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._warning()
        if self.__check_version_range():
            raise ValueError(_("min client version must be less than max one"))
        super(JsonConfig, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("Json Config")
        verbose_name_plural = _("Json Configs")

    def __str__(self) -> str:
        return self.name


class SingletonBaseModel(BaseModel):
    """Used to ensure that a class can only have one concurrent instance."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.__class__.objects.count() == 1:
                raise Exception(_('Only one instance of configurations is allowed.'))
            self.created_time = get_now()
        super().save(*args, **kwargs)


class Configuration(SingletonBaseModel):
    data: dict = {}
    app_name = models.CharField(verbose_name=_("app name"), max_length=255, default=get_app_name)
    version = models.CharField(verbose_name=_("version"), max_length=255, default=get_version)
    social_media_link = models.CharField(verbose_name=_("social media link"), max_length=255, null=True, blank=True)
    config = models.ManyToManyField(verbose_name=_("config"), to=JsonConfig, blank=True)
    deep_link_prefix = models.CharField(verbose_name=_("Deep link prefix"), max_length=255, blank=True, default='')
    maintenance_mode = models.BooleanField(verbose_name=_("maintenance mode"), max_length=255, default=False)
    bypass_verification_email = models.BooleanField(verbose_name=_("bypass verification email"), default=False)

    def __str__(self):
        return f"{self.app_name} ( {self.version} )"

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    @classmethod
    def load(cls) -> dict:
        if cls.data:
            return cls.data
        data, _ = cls.objects.get_or_create()
        cls.data = cls.json_data(data=data)
        return cls.data

    @staticmethod
    def json_data(data) -> dict:
        return {
            "app_name": data.app_name,
            "version": data.version,
            "social_media_link": data.social_media_link,
            "deep_link_prefix": data.deep_link_prefix,
            "maintenance_mode": data.maintenance_mode,
            "bypass_verification_email": data.bypass_verification_email,
            "server_time_zone": data.server_time_zone,
            'config': data.config
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.data = self.json_data(data=self)

    @property
    def server_time_zone(self):
        return settings.TIME_ZONE

    @property
    def server_time(self):
        return standard_response_datetime(get_now())


try:
    APP_CONFIG: dict = Configuration.load()
except Exception as e:
    import logging

    logging.log(level=logging.INFO, msg=e.__str__())
