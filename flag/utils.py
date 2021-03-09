"""General purpose functions that provide utility throughout the application"""
from django.contrib.auth import get_user_model
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_content_type(model_obj):
    return ContentType.objects.get_for_model(model_obj.__class__)


def get_model_object(*, app_name, model_name, model_id):
    """
    Get content object.
    Args:
        app_name (str): name of the app that contains the model.
        model_name (str): name of the model class.
        model_id (int): the id of the model object.

    Returns:
        object: model object according to the parameters passed
    """
    content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
    model_object = content_type.get_object_for_this_type(id=model_id)

    return model_object


def get_user_for_model(obj):
    User = get_user_model()
    for field in obj._meta.fields:
        if field.related_model == User:
            return getattr(obj, field.name)


def process_flagging_request(*, user, model_obj, data):
    """
    Process flagging request and return a response. This handles request for both Django and DRF

    Args:
        user ([type]): The looged in user
        model_obj ([type]): the object being flagged
        data (dict): the data received from the request

    Returns:
        [dict]: response has three keys:
            `status`(int): Non-zero indicates the request failed due to `ValidationError`.
            `msg`(str): response, success message in case request succeeds, reason for
            failure if it doesn't.

            **This key will only be present when request succeeds.**
            `flag`(int): Non-Zero(1) indicates that flag is created.
    """
    FlagInstance = apps.get_model('flag', 'FlagInstance')

    response = {'status': 1}
    try:
        if FlagInstance.objects.set_flag(user, model_obj, **data):
            response['msg'] = _(
                'The content has been flagged successfully. '
                'A moderator will review it shortly.'
                )
            response['flag'] = 1
        else:
            response['msg'] = _('The content has been unflagged successfully.')

        response.update({
            'status': 0
        })
    except ValidationError as e:
        response.update({
            'msg': e.messages
        })

    return response
