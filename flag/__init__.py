VERSION = (1, 1, 0)


def _get_version(version):
    if len(version) > 2:
        str_version = "%s.%s.%s" % version[:3]
    else:
        str_version = "%s.%s" % version[:2]

    return str_version


__version__ = _get_version(VERSION)


default_app_config = 'flag.apps.FlagConfig'
