import django
from django.conf import settings as django_settings
from django.utils.functional import LazyObject

from flag.conf import defaults as flag_settings


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings(flag_settings, django_settings)


_django_version = django.VERSION
DEPRECATED_SETTINGS = {
    'USE_TZ' if _django_version > (4, 0) else None,
    'PASSWORD_RESET_TIMEOUT_DAYS' if _django_version > (3, 0) else None,
    'DEFAULT_CONTENT_TYPE' if _django_version > (2, 2) else None,
    'FILE_CHARSET' if _django_version > (2, 2) else None,
    'USE_L10N' if _django_version > (4, 0) else None,
}


class Settings:
    def __init__(self, *args):
        [
            setattr(self, attr, getattr(item, attr))
            for item in args
            for attr in dir(item)
            if attr == attr.upper() and attr.upper() not in DEPRECATED_SETTINGS
        ]


settings = LazySettings()
