from django.conf import settings as django_settings
from django.utils.functional import LazyObject

from flag.conf import defaults as flag_settings


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings(flag_settings, django_settings)


class Settings(object):
    def __init__(self, *args):
        for item in args:
            for attr in dir(item):
                if attr == attr.upper():
                    setattr(self, attr, getattr(item, attr))


settings = LazySettings()
