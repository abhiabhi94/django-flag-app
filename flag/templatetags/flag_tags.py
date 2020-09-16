from django import template

from flag.models import FlagInstance

register = template.Library()


def get_app_name(obj):
    return type(obj)._meta.app_label


def get_model_name(obj):
    return type(obj).__name__


def has_flagged(user, obj):
    if user.is_authenticated:
        return FlagInstance.objects.has_flagged(user, obj)

    return False


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
        'has_flagged': has_flagged(user, obj),
        'flag_reasons': FlagInstance.reasons
    }
