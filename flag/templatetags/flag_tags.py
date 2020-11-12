from django import template
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from flag.models import Flag, FlagInstance
from flag.conf import settings

register = template.Library()


def get_app_name(obj):
    return type(obj)._meta.app_label


def get_model_name(obj):
    return type(obj).__name__


def has_flagged(user, obj):
    if user.is_authenticated:
        return Flag.objects.has_flagged(user, obj)

    return False


@register.simple_tag(name='get_login_url')
def get_login_url():
    login_url = getattr(settings, 'LOGIN_URL', None)
    if not login_url:
        raise ImproperlyConfigured(_('Django Flag App: LOGIN_URL is not defined in the settings'))
    if not login_url.endswith('/'):
        login_url += '/'
    return login_url


@register.inclusion_tag('flag/flag_form.html')
def render_flag_form(obj, user):
    """
    A template tag used for adding flag form in templates

    To render the flag form for a post model inside the app posts

    Usage: `{% render_flag_form post user %}`
    """
    return {
        'app_name': get_app_name(obj),
        'model_name': get_model_name(obj),
        'model_id': obj.id,
        'user': user,
        'has_flagged': has_flagged(user, obj),
        'flag_reasons': FlagInstance.reasons
    }
